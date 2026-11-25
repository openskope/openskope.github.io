{
  "title": "SKOPE Software Design",
  "type": "docs",
  "wordpress_id": 131,
  "lastmod": "2015-04-29T15:16:25Z",
  "toc_hide": true,
  "aliases": [
    "/skope-software-design/"
  ]
}


The central task of this proposal is to design the synthesis framework needed to process the data to yield the desired information and knowledge. It would involve development of a framework in which different components would extract data, scale them appropriately, apply multiple levels of inference, and report and visualize results in a highly useful form. Inferential procedures at one level, for example, might transform modeled temperature data into a GIS layer for growing season for a key crop. A higher level procedure would produce estimates of agricultural productivity from inferences about the growing season, precipitation, hydrology, and soils.

Not a static, one-off application with a fixed repertoire of data and analytical procedures, SKOPE will be a dynamic framework designed to seamlessly accommodate new data sets as they become available (akin to the ETL workflows that update data warehouses), incorporate classes of environmental data that are not initially included, and expand the analytical, modeling, and inferential operations employed. A key technical challenge usually not addressed in existing systems, will be the need for explicit modeling of both space and time to uncover information about past environments.

We envision that the system would employ a combination of technologies including:
<ul>
	<li><em>“smart” data discovery,</em> based on rich metadata including semantic annotations via ontologies (DataONE already provides this capability);</li>
	<li>relevant <em>data integration technologies, </em>g., based on technologies used in industry such as Extract-Transform-Load [ETL] tools to populate an integrated data warehouse, or novel technologies from academia and computer science to facilitate knowledge-based information integration and semantic mediation;</li>
	<li><em>workflow and process integration technologies</em>, e.g., through scientific workflow systems such as Kepler, Taverna, VisTrails, etc. (co-PI Ludäscher is one of the co-founders of the open-source Kepler system, and workflow tools are part of the DataONE ITK);</li>
	<li><em>provenance management techniques</em>, to capture, query, and analyze data dependencies and lineage information (provenance capabilities are being integrated into DataONE); and</li>
	<li><em>knowledge representation, modeling integration, and reasoning techniques</em>, where state-of-the-art and emerging new techniques for environmental modeling (e.g., “declarative modeling”) would need to be considered (Villa et al. 2009; Lloyd et al. 2011; David et al. 2013).</li>
</ul>
We recognize that our vision for SKOPE is very ambitious and probably is only feasible if we develop a very clear understanding of its scope and key use cases. The development of specific scientific use cases will be crucial for the success of the project. In order to gather requirements and work towards an initial design, a series of working meetings will take place. During these meetings, end-user example scenarios will be presented and new ones developed. Relevant data and existing methods and tools for implementing the desired analyses will also be identified. In addition to potential SKOPE end-users identified through our Needs Assessment, experts familiar with the capabilities and limitations of relevant technologies mentioned above would be invited to the working meetings to inform and guide ideas for the tool design.

We expect that the tool will be able to automatically discover new data sources (documented with appropriate metadata) as they are added to one of the DataONE member nodes. (One way this can be achieved is with a publish-subscribe model in which a user chooses concepts and domain areas of interest from a controlled vocabulary or ontology). We also expect that the design will be sufficiently flexible that it will be possible for others to add processing modules with minimal need for central intervention. By adopting a scientific workflow paradigm, that is, where processing interfaces are well specified to facilitate community contributions, users will be able to develop new analysis methods and deploy and share them as scientific workflows.

SKOPE must account for the fact that there may be more than one reasonable environmental reconstruction for a given set of data. These different reconstructions operationalize different models of the environment. Thus, the answer to a query may include multiple possible scenarios and outcomes (a.k.a. “possible worlds” in knowledge representation) and have associated with them varying degrees of uncertainty. Indeed, nearly any environmental knowledge claim is the result of long chains of analytical and inferential steps (inference pathways), each of which has embedded assumptions (Figure 3). Through the incorporation of methods from scientific workflows, provenance, and knowledge-representation and reasoning research by Ludäscher, we expect to be able to present the results of alternative inferential pathways that lead to different results from the same initial data. We believe that the resulting provenance and knowledge graphs will be invaluable for users who will need to consider these alternative reconstructions.

In general, the tool would be able to report the provenance of the resulting data products and information, including both citations of the data sources utilized and documentation of the synthetic procedures employed. The provenance would include both a human-readable report and a more precise computer-readable audit trail that would permit the replication of results. It would automatically also provide a citation for the resulting reconstruction.

The interface will certainly be map-based and would likely have different faces for scientific and general public users of SKOPE and for its data providers. Outputs could include spatial and temporal visualizations, tabular data, or GIS layers. The software will, of course, be designed to record usage of the tool. It will include the ability for users to opt-in to participate in follow-up assessments of the tool.
