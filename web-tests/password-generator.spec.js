const { test, expect } = require("@playwright/test");

test("loads the Python runtime", async ({ page }) => {
  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();
  await expect(generateButton).toHaveText("Generate password");
  await expect(page.locator("#form-error")).toHaveText("");
});

test("generates one default password", async ({ page }) => {
  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();

  await generateButton.click();

  const passwords = page.locator(".password-value");

  await expect(passwords).toHaveCount(1);

  const password = await passwords.first().textContent();

  expect(password).toHaveLength(20);
});

test("generates multiple passwords", async ({ page }) => {
  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();

  await page.locator("#count").fill("3");
  await generateButton.click();

  await expect(page.locator(".password-value")).toHaveCount(3);
});

test("excludes ambiguous characters", async ({ page }) => {
  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();

  await page.locator("#count").fill("10");
  await page.locator("#exclude-ambiguous").check();
  await generateButton.click();

  const passwords = page.locator(".password-value");

  await expect(passwords).toHaveCount(10);

  for (const password of await passwords.allTextContents()) {
    expect(password).not.toMatch(/[0O1lI]/);
  }
});

test("rejects disabling every character type", async ({ page }) => {
  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();

  await page.locator("#lowercase").uncheck();
  await page.locator("#uppercase").uncheck();
  await page.locator("#digits").uncheck();
  await page.locator("#symbols").uncheck();

  await generateButton.click();

  await expect(page.locator("#form-error")).toHaveText(
    "At least one character type must be enabled.",
  );

  await expect(page.locator(".password-value")).toHaveCount(0);
});

test("rejects a password length below the minimum", async ({ page }) => {
  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();

  await page.locator("#length").fill("14");
  await generateButton.click();

  await expect(page.locator("#form-error")).toHaveText(
    "Password length must be at least 15.",
  );

  await expect(page.locator(".password-value")).toHaveCount(0);
});

test("rejects a password count above the maximum", async ({ page }) => {
  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();

  await page.locator("#count").fill("101");
  await generateButton.click();

  await expect(page.locator("#form-error")).toHaveText(
    "Number of passwords must be between 1 and 100.",
  );

  await expect(page.locator(".password-value")).toHaveCount(0);
});

test("copies an individual password", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"], {
    origin: "http://127.0.0.1:8000",
  });

  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();
  await generateButton.click();

  const password = await page.locator(".password-value").first().textContent();

  await page.locator(".copy-button").first().click();

  await expect(page.locator("#copy-status")).toHaveText("Password 1 copied.");

  const clipboardText = await page.evaluate(() =>
    navigator.clipboard.readText(),
  );

  expect(clipboardText).toBe(password);
});

test("copies all generated passwords", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"], {
    origin: "http://127.0.0.1:8000",
  });

  await page.goto("/docs/");

  const generateButton = page.locator("#generate-button");

  await expect(generateButton).toBeEnabled();

  await page.locator("#count").fill("3");
  await generateButton.click();

  const passwords = await page.locator(".password-value").allTextContents();

  await page.locator("#copy-all").click();

  await expect(page.locator("#copy-status")).toHaveText(
    "All passwords copied.",
  );

  const clipboardText = await page.evaluate(() =>
    navigator.clipboard.readText(),
  );

  expect(clipboardText.split(/\r?\n/)).toEqual(passwords);
});
