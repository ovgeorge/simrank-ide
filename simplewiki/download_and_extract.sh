wget http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz > simplewiki-latest-page.sql.gz --progress-bar
#wget -c http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz
gunzip -c *page.sql.gz > page.sql
wget http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pagelinks.sql.gz > simplewiki-latest-pagelinks.sql.gz --progress-bar
#wget -c http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pagelinks.sql.gz
gunzip -c *pagelinks.sql.gz > pagelinks.sql
wget http://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-categorylilnks.sql.gz > simplewiki-latest-categorylinks.sql.gz --progress-bar
gunzip -c *categorylinks.sql.gz > categorylinks.sql
