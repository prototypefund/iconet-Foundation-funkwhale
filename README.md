# Iconet - Funkwhale

Funkwhale is an audio service that supports [ActivityPub](https://activitypub.rocks/).
As a proof-of-concept, we added [iconet-specific metadata](https://docs.iconet-foundation.org/en/latest/specification.html#required-iconet-meta-data) to audio tracks.

When iconet-supporting clients receive an [ActivityPub](https://www.w3.org/TR/activitypub/)-formatted audio track packet, they can use the iconet metadata to render a fallback presentation.
Currently, those can be viewed with our [modified Mastodon fork](https://codeberg.org/iconet-Foundation/mastodon) and with our custom prototype, [NetA](https://codeberg.org/iconet-Foundation/prototype-ExampleNetA) with packets being transported via a [bridge](https://codeberg.org/iconet-Foundation/bridge).

For the current state of the iconet spec, check [our readthedocs](https://docs.iconet-foundation.org/).

Note: For the setup, in the file `manifest.jsonld`, you additionally need to prefix the `@id` URIs with the funkwhale hostname you are using and add the hostname to the field `allowedSources`.

# Funkwhale

[![The Funkwhale logo](./front/src/assets/logo/logo-full-500.png)](https://funkwhale.audio)

Funkwhale is a platform for uploading, sharing, and publishing audio content across the federated web. Curate your music library, listen to podcasts, or create your own content and share it with the world.

## Contribute

Want to help make Funkwhale even better? We welcome contributions from across the community. Whether you are a designer, a translator, a technical writer, or a developer, we look forward to seeing your work!

You can find contribution information in our [documentation hub](https://docs.funkwhale.audio).

- [Developer guides](https://docs.funkwhale.audio/developers/index.html)
- [Contributor guides](https://docs.funkwhale.audio/contributing.html)

## Get help

Got a question or need help? Head over to our [forum](https://forum.funkwhale.audio/t/support) and open up a discussion.

## Report a security issue

If you find a security issue or vulnerability, please report it on our [GitLab instance](https://dev.funkwhale.audio/funkwhale/funkwhale/-/issues). When you open your issue, select the **This issue is confidential and should only be visible to team members with at least Reporter access** option. This ensures developers can verify and patch the issue before disclosing it.

## Code of conduct

The Funkwhale collective adheres to a [code of conduct](https://funkwhale.audio/en_US/code-of-conduct) in all our community spaces. Please familiarize yourself with this code and follow it when participating in discussions in our spaces.
