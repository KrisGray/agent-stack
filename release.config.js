export default {
  branches: ["main"],
  plugins: [
    // Pre-1.0: breaking changes bump minor, not major. Flip to standard
    // rules (remove the override) when the package goes 1.0.
    [
      "@semantic-release/commit-analyzer",
      {
        preset: "conventionalcommits",
        releaseRules: [{ breaking: true, release: "minor" }],
      },
    ],
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
