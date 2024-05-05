# AI_Rankings

## Overview

This repository contains an alternative approach to ranking universities based on research output, inspired by the methodology used by [csrankings.org](https://csrankings.org/). While csrankings.org employs a weighted metric that emphasizes author contributions, this project proposes a different approach aimed at highlighting institutional contributions as a whole when assigning the university rankings.

## Appraoch

### CSRankings.org Approach:

- **Adjusted counts by co-author**: csrankings.org ranks universities based on a weighted metric that considers the number of publications and weights them according to author contributions. According to the CSRankings FAQ: each publication is counted exactly once, with credit adjusted by splitting evenly across all co-authors. This approach makes it impossible to boost rankings simply by adding authors to a paper. 

However, if more authors from the same institution were added to the same paper, then the overall proportion of the faculty from that particular institution would actually show a greater dominance. Of the total score of 1 per publication, a greater share of the point would go to the institution which added more co-authors, and subsequently impact the rankings when cumulated over a large number of publications. In this perspective, it appears that the co-author weighting contradicts the prevention of boosting rankings through co-authoring.

### Alternative Approach:

- **Counts by institution**: Since the goal of the algorithm is to rank institutions based of contributions to research publications, one method to ensure fairness in calculation is to give equal credit to all institutions contributing to any particular publication, regardless the number of co-authors. For any publication, we can assign a score of 1 to each contributed organization.

- **Adjusted counts by co-author**: With the above method, one potential drawback would be the inconsistency in overall scores of publications, ie 1 if all authors are from the same school whereas other intermural papers will display a score above 1. While the effects of this inconsistency is to be evaluated, normalizng each publication with this approach should not effect the overall credit distribution.


## Methodology

### Data Collection:

Similar to CSRankings, the publication data is taken from the DBLP database as a regularly updated XML file. Reference tables are retrieved from the CSRankings GitHub repository which includes relational data between faculty and affiliation, as well as the location details of the recorded institutions.

### Data Processing:

- **Mapping**: The entire XML file is parsed with Python and key information such as title, year, conference, and list of authors are extracted. Then, the corresponding affiliations and the location information are added to the table, which is eventually compiled and saved into a comprehensive spreadsheet.

- **Filtering**: With the combined spreadsheet, different insights can be analyzed by performing boolean indexing on the spreadsheet to obtaing the publication information matching the criteria.

For this project, we specifically selected a total of 14 scientific conferences including but not limited to CVPR, ICML, and NIPS to represent the current state of research in AI-related fields.

By filtering the spreadsheet by year, conference, and institution name, we get a smaller table with a row count we can use as our ranking metric.

### Visualizations:

In creating a combined spreadsheet, we enable visualizations to be made with greater convenience when looking at other insights such as distribution by conference, top N institutions by criteria, or yearly publications by school etc.


## Considerations and Advantages

- **Fairness**: The proposed approach promotes fairness by ensuring that all affiliated institutions are represented equally in the rankings, regardless of their research output.

- **Simplicity**: By removing the normalization calculation we can count the number of occurences of our target institution(s) to determine how many publications the institution has made a contribution towards, regardless of significance of contribution, which is very difficult to gauge objectively. This method is much easier to obtain an integer value to assign a rank.

- **Collaboration**: By recognizing the collective effort involved in research projects and treating all affiliated institutions equally, this approach may emphasize the collaborations among multiple organizations and give more credit to the contributions of less represented institutions.
