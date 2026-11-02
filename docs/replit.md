# Antithesis in Replit

## Customer setup

* Add secrets:
  * `ANTITHESIS_API_KEY`
  * `ANTITHESIS_TENANT`
  * `ANTITHESIS_REPOSITORY` (GAR repository url)
  * `ANTITHESIS_GAR_KEY`

  Either to a specific App ({App} -> Tools -> Secrets), or to your personal account (Profile -> Account secrets) and then linked to individual Apps.
* Add the plugin: Customization → Skills → Add.
  * If Add offers "Add from GitHub", enter:

     ```text
     https://github.com/antithesishq/antithesis-plugin/tree/main/plugins/antithesis/skills/antithesis
     ```

  * Otherwise, choose "Upload a skill", and upload this zip:

     ```bash
     git clone https://github.com/antithesishq/antithesis-plugin
     cd antithesis-plugin/plugins/antithesis/skills
     (cd antithesis && zip -r ../antithesis.zip .)
     ```

## Usage

E.g.:

```text
/antithesis "write a test for rqlite"
```
