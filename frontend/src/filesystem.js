import * as BrowserFS from "browserfs";

let fs = null;

export function initFS() {
  return new Promise((resolve, reject) => {
    BrowserFS.configure(
      {
        fs: "InMemory",
        options: {},
      },
      (err) => {
        if (err) return reject(err);

        fs = BrowserFS.BFSRequire("fs");

        // create default file
        if (!fs.existsSync("/main.py")) {
          fs.writeFileSync(
            "/main.py",
            `print("Hello from Windsurf-style IDE")`
          );
        }

        resolve(fs);
      }
    );
  });
}

export function getFS() {
  return fs;
}
