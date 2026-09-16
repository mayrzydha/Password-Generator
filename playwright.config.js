const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./web-tests",
  timeout: 60_000,

  expect: {
    timeout: 30_000,
  },

  use: {
    baseURL: "http://127.0.0.1:8000",
    headless: true,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },

  webServer: {
    command: "python -m http.server 8000",
    url: "http://127.0.0.1:8000/docs/",
    reuseExistingServer: true,
    timeout: 10_000,
  },
});
