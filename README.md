# [wip] Parsing dialogues in Prequel Star Wars movies

## From:

### 1. [getyarn.io](./yarn)
   - links to:
     - thumbnails
     - video
   - actual quote text
   - time

### 2. [ISDB](./scripts)
   - which character speaking

### 3. [starwars.fandom.com](./scripts/parsed_scripts/characters_fandom)
   - based on ISDB data get link to character 

### 4. [Merge all the information together](./archived/merge) (todo)

Problem may be to identify which quote is which since there may be typos and the yarn quotes are usually
shorter than the ones in the scripts, where one quote may be multiple sentences long.

An optimization may be to take into account that the [parsed scripts](./scripts/parsed_scripts) are saved
in order, which means you can linearly (maybe even zip) and after finding remove the found script to 
make the necessary search in the next quote shorter.

Some package must be used to fuzzy match quotes!

### 5. [star-wars-analysis](./star-wars-analysis)

Credit goes to the LA Times' team for open-sourcing their
[star-wars-analysis](https://github.com/datadesk/star-wars-analysis)
repository, which thanks to the raw, manual man-power involved I decided to treat as
the source of truth for dialogues, as well as it provided the data
of who is speaking to whom.


### 6. Create website (todo)(separate repo)

Statically generated for each quote. With side shots of the speaking character
on the left in the background and the recipient on the right (if any).

Search:
- download big json file and search on client
- Lambda function with Tantivy on AWS
- download big json file, but while downloading use Lambda function?
  - needs testing to see how large the file is / how long it will be downloading

On each quote website:
- Movie part
- Images with characters
  - characters with links to wookiepedia
- Quote
- Time
- Yarn link / iFrame
- generate subreddit with each quote as post? and add link to post for discussion?
  - dont archive posts
- suggest changes on GitHub if there is an error!
 
Weird idea:

Get an image where each x line is an average of each frame, and set the background
color based on that image.


### 6. Use in bot (todo) (separate repo)
