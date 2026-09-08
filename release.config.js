export default {
  branches: ["main"],
  plugins: [
    ["@semantic-release/commit-analyzer", { preset: "conventionalcommits" }],
    ["@semantic-release/release-notes-generator", { preset: "conventionalcommits" }],
    [
      "@semantic-release/changelog",
      { changelogFile: "CHANGELOG.md", changelogTitle: "# Changelog" },
    ],
    ["@semantic-release/npm", { provenance: true }],
    ["@semantic-release/git", { assets: ["package.json", "CHANGELOG.md"] }],
    ["@semantic-release/github", { successComment: false }],
  ],
};
