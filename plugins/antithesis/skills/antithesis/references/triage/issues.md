# Report issues

Report one issue per root cause, even if several properties failed from it.

Use the destination and format the user specified. Without a format, use the one below; without a destination, print the report in the session. The format is written for GitHub; adapt its syntax for other destinations.

Write for a maintainer who knows this codebase but not Antithesis or this run. Lead with what's wrong and where. Explain one representative occurrence in the code's terms. Put supporting evidence in a collapsed `<details>` block. Don't describe how you investigated.

```
# <title>

<antithesis property name that failed>

<description of bug>

## Reproduction

<reproducer>

## Details

* Antithesis run: [`<run id>`](<run link>)
* Input hash: `<input hash>`
* vtime: `<vtime>`
* Version: <git hash>

<duplicate_details>
```

<run link> is `https://<tenant>.antithesis.com/run?run_id=<run id>`, with the tenant from `snouty settings show`.

## Reproducer

Put a reproducer in <reproducer>: code the maintainer can run to reproduce the bug without Antithesis. Prose instructions are not reproducers. Run it and confirm it reproduces the bug before including it. Don't commit it to the repository.

If a reproducer would be too hard to write, silently leave out the Reproduction section.

## Duplicates

Search the destination for existing issues before reporting.

If the bug already exists, edit the issue to add a bullet point to its <duplicate_details>.

<duplicate_details> has the following format:

```
## Other Antithesis runs

<details><summary>Details</summary>
<p>

* [`run id`](run link)

</p>
</details>
```

and is present only if there are duplicates, so you may have to create it. Each bullet holds only the linked `run id`.
