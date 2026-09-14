const PYODIDE_INDEX_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/";

const form = document.querySelector("#password-form");

const lengthInput = document.querySelector("#length");
const countInput = document.querySelector("#count");

const lowercaseInput = document.querySelector("#lowercase");
const uppercaseInput = document.querySelector("#uppercase");
const digitsInput = document.querySelector("#digits");
const symbolsInput = document.querySelector("#symbols");
const excludeAmbiguousInput = document.querySelector("#exclude-ambiguous");

const generateButton = document.querySelector("#generate-button");
const formError = document.querySelector("#form-error");

const resultsSection = document.querySelector("#results-section");
const passwordResults = document.querySelector("#password-results");

const copyAllButton = document.querySelector("#copy-all");
const copyStatus = document.querySelector("#copy-status");

let pyodide = null;
let pythonGeneratePassword = null;

let generatedPasswords = [];

let minLength = null;
let maxPasswordCount = null;

async function fetchMainSource() {
  const candidatePaths = window.location.pathname.includes("/docs/")
    ? ["../main.py", "main.py"]
    : ["main.py", "../main.py"];

  for (const path of candidatePaths) {
    try {
      const response = await fetch(path, {
        cache: "no-store",
      });

      if (response.ok) {
        return await response.text();
      }
    } catch {
      // Try the next path.
    }
  }

  throw new Error("Unable to load main.py.");
}

async function initializePython() {
  try {
    pyodide = await loadPyodide({
      indexURL: PYODIDE_INDEX_URL,
    });

    const mainSource = await fetchMainSource();

    pyodide.FS.writeFile("/home/pyodide/main.py", mainSource);

    pyodide.runPython(`
import sys

if "/home/pyodide" not in sys.path:
    sys.path.insert(0, "/home/pyodide")

import main
import secrets

secrets.token_bytes(32)
`);

    pythonGeneratePassword = pyodide.runPython("main.generate_password");

    minLength = Number(pyodide.runPython("main.MIN_LENGTH"));

    maxPasswordCount = Number(pyodide.runPython("main.MAX_PASSWORD_COUNT"));

    const defaultLength = Number(pyodide.runPython("main.DEFAULT_LENGTH"));

    const defaultPasswordCount = Number(
      pyodide.runPython("main.DEFAULT_PASSWORD_COUNT"),
    );

    const applicationVersion = String(pyodide.runPython("main.VERSION"));

    lengthInput.min = String(minLength);
    lengthInput.value = String(defaultLength);

    countInput.min = "1";
    countInput.max = String(maxPasswordCount);
    countInput.value = String(defaultPasswordCount);

    generateButton.disabled = false;
    generateButton.removeAttribute("aria-busy");
    generateButton.textContent = "Generate password";

    console.info(
      `Password Generator ${applicationVersion}: Python runtime ready.`,
    );
  } catch (error) {
    console.error(error);

    generateButton.disabled = true;
    generateButton.removeAttribute("aria-busy");
    generateButton.textContent = "Python runtime unavailable";

    formError.textContent =
      "Unable to load the Python runtime. Please reload the page.";
  }
}

function getOptions() {
  return {
    includeLowercase: lowercaseInput.checked,
    includeUppercase: uppercaseInput.checked,
    includeDigits: digitsInput.checked,
    includeSymbols: symbolsInput.checked,
    excludeAmbiguous: excludeAmbiguousInput.checked,
  };
}

function validateSettings(length, count, options) {
  if (!Number.isInteger(length) || length < minLength) {
    return `Password length must be at least ${minLength}.`;
  }

  if (!Number.isInteger(count) || count < 1 || count > maxPasswordCount) {
    return (
      "Number of passwords must be between " + `1 and ${maxPasswordCount}.`
    );
  }

  if (
    !options.includeLowercase &&
    !options.includeUppercase &&
    !options.includeDigits &&
    !options.includeSymbols
  ) {
    return "At least one character type must be enabled.";
  }

  return "";
}

function generatePassword(length, options) {
  if (pythonGeneratePassword === null) {
    throw new Error("Python runtime is not ready.");
  }

  return String(
    pythonGeneratePassword(
      length,
      options.includeLowercase,
      options.includeUppercase,
      options.includeDigits,
      options.includeSymbols,
      options.excludeAmbiguous,
    ),
  );
}

function clearResults() {
  generatedPasswords = [];

  passwordResults.replaceChildren();
  resultsSection.hidden = true;
  copyStatus.textContent = "";
}

function createPasswordItem(password, index) {
  const item = document.createElement("div");
  item.className = "password-item";

  const value = document.createElement("span");
  value.className = "password-value";
  value.textContent = password;

  value.setAttribute("aria-label", `Password ${index + 1}`);

  const copyButton = document.createElement("button");
  copyButton.className = "copy-button";
  copyButton.type = "button";
  copyButton.textContent = "Copy";

  copyButton.addEventListener("click", async () => {
    const copied = await copyText(password);

    copyStatus.textContent = copied
      ? `Password ${index + 1} copied.`
      : "Unable to copy password.";
  });

  item.append(value, copyButton);

  return item;
}

function renderPasswords(passwords) {
  passwordResults.replaceChildren();

  passwords.forEach((password, index) => {
    passwordResults.append(createPasswordItem(password, index));
  });

  resultsSection.hidden = false;
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  formError.textContent = "";
  copyStatus.textContent = "";

  const length = Number(lengthInput.value);
  const count = Number(countInput.value);
  const options = getOptions();

  const validationError = validateSettings(length, count, options);

  if (validationError) {
    formError.textContent = validationError;
    clearResults();
    return;
  }

  try {
    generatedPasswords = Array.from({ length: count }, () =>
      generatePassword(length, options),
    );

    renderPasswords(generatedPasswords);
  } catch (error) {
    console.error(error);

    clearResults();

    formError.textContent =
      "Unable to generate a password with the selected settings.";
  }
});

copyAllButton.addEventListener("click", async () => {
  if (generatedPasswords.length === 0) {
    return;
  }

  const copied = await copyText(generatedPasswords.join("\n"));

  copyStatus.textContent = copied
    ? "All passwords copied."
    : "Unable to copy passwords.";
});

window.addEventListener("beforeunload", () => {
  if (
    pythonGeneratePassword !== null &&
    typeof pythonGeneratePassword.destroy === "function"
  ) {
    pythonGeneratePassword.destroy();
  }
});

initializePython();
