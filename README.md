# [wip] Parsing dialogues in Prequel Star Wars movies

## From:

### 1. getyarn.io ([yarn](./yarn))
   - links to:
     - thumbnails
     - video
   - actual quote text
   - time

### 2. ISDB ([scripts](./scripts))
   - which character speaking

### 3. starwars.fandom.com (todo)
   - based on ISDB data get link to character 

### 4. Merge all the information together (todo)

Problem may be to identify which quote is which since there may be typos and the yarn quotes are usually
shorter than the ones in the scripts, where one quote may be multiple sentences long.

An optimization may be to take into account that the [parsed scripts](./scripts/parsed_scripts) are saved
in order, which means you can linearly (maybe even zip) and after finding remove the found script to 
make the necessary search in the next quote shorter.

Some package must be used to fuzzy match quotes!

### 5. Use in bot (todo)
