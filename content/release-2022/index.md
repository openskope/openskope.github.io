{
  "title": "SKOPE Release Info",
  "type": "docs",
  "wordpress_id": 711,
  "lastmod": "2023-08-09T20:55:46Z",
  "toc_hide": true,
  "aliases": [
    "/announcement/"
  ]
}

{{< skope-figure src="wp-content/uploads/2021/11/HeaderBase-Color-2021v4.png" alt="" eager=true align="center" >}}

<strong>7 May 2022.  <mark class="has-inline-color has-red-color skope-announcement">We have released the production version of SKOPE (Synthesizing Knowledge of Past Environments)</mark></strong>, an NSF-funded, online tool that enables users to easily explore, visualize, analyze, and synthesize knowledge about past environments.&nbsp; Users set a location and time period of interest and SKOPE provides free analytical and graphical access to long-term, high-resolution environmental data reaching back more than 2000 years. We expect that this tool may be of value to <mark class="has-inline-color has-red-color skope-announcement"><strong>archaeologists</strong>, <strong>ecologists, historians, geographers, planners and other professionals</strong></mark> interested in past landscapes or in comparing environmental conditions at the same place at different times or between different places.

Notably, SKOPE provides access to [PaleoCAR]({{< relref "/paleocar" >}}), which offers annual retrodictions of precipitation and temperature at 800m spatial resolution, for the Southwest US for the last 2000 years. At a coarser spatial resolution (~50km), SKOPE offers annual reconstructions of the Palmer Modified Drought Index (PMDI; the successor to the Palmer Drought Severity Index or PDSI) for the contiguous 48 US states, also for the last 2000 years. SKOPE also provides ready access to US elevation data through the SRTM90 Elevation Model for the contiguous 48 US states.&nbsp; SKOPE centralizes access to these datasets, which would otherwise be quite difficult and require considerable technical expertise to obtain.&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

This release of SKOPE includes a number of important features suggested by users of our prototype app.  While we have extensively tested SKOPE, this is a complex software application that is only recently completed.  <strong>Please [notify us](mailto:skope-team@googlegroups.com) if you run into any problems or discover any bugs.</strong>  We look forward to adding additional datasets and making software improvements as time and funding allow.

Please, take a few minutes to experiment with the [**SKOPE App**](https://app.openskope.org/). Please also pass on this announcement to other individuals or user communities that might be interested.

<strong>Using SKOPE's intuitive user interface</strong>, users

1. Select a paleoenvironmental dataset,
1. Define a study area (point, circle rectangle, or arbitrary polygon),
1. Specify a temporal interval and variable to analyze,
1. Receive:
    - An animated time-series display of the spatial distribution of retrodicted values
    - A graph and descriptive statistics summarizing the retrodicted values through time. Optionally, the graph can be smoothed and displayed as Z-scores.&nbsp;

All work conducted&nbsp; in SKOPE can be downloaded and sessions saved for later access.&nbsp; Detailed metadata, including citation recommendations, are available for each dataset. While we have designed SKOPE to be easy to use, there is a detailed [SKOPE User Guide]({{< relref "/users-guide" >}}).&nbsp; The SKOPE project is described at our website ([https://openskope.org]({{< relref "/" >}})).

<strong>Possible Questions SKOPE Can Help Answer</strong>

- <strong><em>Archaeology &amp; History:</em></strong> What is the climatic context of major transitions or events observed in my study area?
- <strong><em>Ecology:</em></strong> What are the long term legacy effects of past climates on current animal or plant&nbsp; distributions?
- <strong><em>Planning:</em></strong> For the area of my management responsibility, during the last 1000 years how often were drought conditions as bad or worse than they have been in the last 20 years?
- <strong><em>Geographers:</em></strong> How have regional patterns of shifts in agricultural practices been influenced by spatial and temporal patterns of drought?

{{< skope-figure src="wp-content/uploads/2022/05/Zuni-Graph-2022-05-04_15-44-35.png" alt="Retrodicted water-year precipitation around the protohistoric Zuni towns, AD 1450–1700, smoothed with a 21-year centered running average; 1680 is highlighted." width="635" caption="Retrodicted Water year precipitation for the area encompassing the protohistoric Zuni towns in New Mexico, AD 1450-1700, smoothed with a 21 year centered running average. The year of the Pueblo Revolt, 1680, is highlighted.." >}}

<strong>We offer a single example</strong> of SKOPE’s capabilities, inspired by a [request from historian Richard Flint]({{< relref "/research-questions" >}}) who wanted to examine whether regional climate influenced the nature of early interactions between the Spanish and the indigenous Pueblo people in New Mexico.&nbsp; If we look at the 300km2 portion of the Zuni River drainage occupied by Zuni people from about AD 1400 to 1692 (graph above), we can observe several things in the smoothed annual graph of water-year precipitation. First, in the Spanish invasion of 1540, Vázquez de Coronado arrived in the midst of a 50+ year period of good rainfall. However, Juan de Oñate’s colonization of New Mexico, begun in 1598, came near the end of 40 years of relatively poor rainfall. And although 1680 was a wet year, the Pueblo Revolt in August of that year occurred near the end of 30 year period of unusual dryness. Repeating this analysis for the Rio Grande valley reveals very similar rainfall patterns.

{{< skope-figure src="wp-content/uploads/2022/05/Tewa-Basin-1540-2022-05-04_15-57-37.png" alt="Map of retrodicted water-year precipitation in millimeters in AD 1540 for the northern Rio Grande area of the Tewa Pueblos." caption="_Retrodicted water year precipitation (in mm) in AD 1540 for the northern Rio Grande area of the Tewa Pueblos ._" >}}

We welcome your feedback on the SKOPE app, including how you have used it, any bugs you’ve discovered, the quality of the user experience, and ideas for extending its capabilities in the future.&nbsp;

[<strong>Try the SKOPE App</strong>](https://app.openskope.org/)

We hope you find it useful in your research.&nbsp; Thank you for your interest.

<strong>The SKOPE Team</strong>: R. Kyle Bocinsky, Andrew Gillreath-Brown, Keith Kintigh, Ann Kinzig, Timothy A. Kohler, Allen Lee, Bertram Ludaescher, and Timothy McPhillips.

<em>This material is based upon work supported by the National Science Foundation under Grant Nos. SMA 1439591 and 1637189 to Arizona State University, SMA 1439603 and 1637155 to the University of Illinois at Urbana-Champaign, and SMA 1439516 and 1637171 to Washington State University.</em>
