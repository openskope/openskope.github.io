{
  "title": "SKOPE: Prototype App User's Guide",
  "type": "docs",
  "wordpress_id": 621,
  "lastmod": "2021-08-19T21:29:42Z",
  "toc_hide": true,
  "aliases": [
    "/skope-prototype-app-users-guide/"
  ]
}


> **Prototype archive.** This page documents an earlier version of SKOPE.
> See [project news and history]({{< relref "/news" >}}) for context, or use
> the [SKOPE application page]({{< relref "/use-skope" >}}) to get started.

<div class="wp-block-image"><figure class="alignright"><img src='{{< siteurl "wp-content/uploads/2018/09/skope-300x169.png" >}}' alt="" class="wp-image-527"/></figure></div>



<p><strong><br>Alpha Release.</strong> The current SKOPE application is an alpha release, meaning that while we believe the results to be accurate, the application has not been thoroughly tested and is subject to frequent change.&nbsp; To run the application in another window, click <a href='http://app.openskope.org' target="_blank" rel="noreferrer noopener">here</a>.&nbsp; The SKOPE team is constantly adding features so all details of the application's operations may not be reflected in this documentation.&nbsp; We have a substantial backlog of features slated for development.&nbsp; At this point we would be particularly grateful for bug reports and reports that data does not seem to be displayed or graphed correctly.&nbsp;&nbsp;&nbsp;Please send comments and queries to <a href='mailto:kintigh@asu.edu'>Keith Kintigh</a>.</p>



<p><strong>Discover.&nbsp;</strong> The SKOPE application starts on the Discover tab, from which you select the paleoenvironmental dataset you wish to explore.&nbsp; You can do that either by paging through the descriptions on the right pane, or by filtering the available datasets (using the left pane) by the class of variable that is of interest (e.g. precipitation), the time period of interest,&nbsp;whether the dataset is published, or the geographic area of interest.&nbsp; When filters have been selected, only those datasets matching (i.e. overlapping) your conditions will be shown.</p>



<p>To select a dataset simply click on its title.&nbsp; If this is your first view of the dataset, you will be taken to its <strong>Info</strong> page.</p>



<figure class="wp-block-image"><img src='{{< siteurl "wp-content/uploads/2018/06/Discover.png" >}}' alt="" class="wp-image-493"/></figure>



<p><strong>Info.</strong> The info tab provides metadata on the selected dataset.&nbsp; This includes the title and author, a brief summary (including spatial and temporal resolution), keywords, and additional information.</p>



<figure class="wp-block-image"><img src='{{< siteurl "wp-content/uploads/2018/06/Info.png" >}}' alt="" class="wp-image-491"/></figure>



<p><strong>Variable, Temporal, and Spatial Selection (Map and Graph View)</strong>. In the map and graph view, selection of the variable, time period, and geographic area is done on the left pane.&nbsp; The specific&nbsp;<em> variables</em> available in the selected dataset (as selected on the Discover tab and as displayed in the title line at the top of the window, ) are listed at the top of the left pane.&nbsp; A variable's display properties (e.g. opacity) can be modified by clicking the Style icon to the right of the variable name (or hidden by again clicking on the style icon).&nbsp; &nbsp;Current display properties include only Opacity. Overlay Range, truncating the range of values displayed with different colors, will be implemented soon.&nbsp; When overlay range is implemented, the values to be displayed are narrowed using the left and right sliders or may be typed in.&nbsp; Values less than the selected lower range limit will display the color of that lower limit, and similarly for values above the upper range limit.</p>



<div class="wp-block-image"><figure class="alignleft"><img src='{{< siteurl "wp-content/uploads/2018/06/Select.png" >}}' alt="" class="wp-image-494"/></figure></div>



<p>The <em>temporal</em> control defaults to the full temporal range available in the dataset.&nbsp; This may be narrowed by typing over the "from" and "to" dates displayed to the right, by moving the left and right (lower and upper bound) sliders, or having clicked on one of the text dates, by incrementing or decrementing the value with the arrows that appear.&nbsp; Datasests with annual resolution display the year.&nbsp; Datasets (e.g. PRISM) with monthoy resolution will appear as YYYYMM.</p>



<p>The <em>spatial</em> selection is done by zooming using the + and - , and panning (with the Hand icon selected [outlined gray]) on the map at the bottom of the left pane to the general area of interest.&nbsp; The red outlined area in that map indicates the area for which the selected dataset has data.&nbsp; Having zoomed and panned to the general area, a particular geographic&nbsp; selection may be defined using the point selection icon or the rectangle selection icon and clicking and dragging to define a rectangle (circle and polygon selection forthcoming).</p>



<p><strong>Map View.&nbsp;&nbsp;</strong>The map view shows a map that is colored based on the value of the selected variable, for the selected area, for the first temporal interval (e.g., year) of the selected temporal range.&nbsp; The selected area is outlined in blue. In the legend, the X&nbsp;indicates transparent color.&nbsp; In most cases (e.g., precipitation), the variable values are in a time series (i.e. a differ value for each year) and the map visualization can be shown for any time step (e.g. year) or run as an animation using the controls under the large map on the right, using the temporal range selected.&nbsp; Or, you can jump to a specific year by typing over the year displayed below the big map on the right and pressing Enter or Tab.&nbsp; Spatial, temporal and variable selections can be made at any time in the left pane.</p>



<p><em>Note.&nbsp;</em>The&nbsp; map view legend reflects the overlay color (indicating the selected variables value) <em>assuming that the variable's overlay opacity is set to 100% and neglecting the effect of the base map</em>.&nbsp; To effectively compare the displayed overlay colors on the map, you may need to increase the variable's opacity.&nbsp; To do that&nbsp; click on [Style] (to be replaced by a gear) and move the opacity slider to the right.</p>



<figure class="wp-block-image"><img src='{{< siteurl "wp-content/uploads/2018/06/Map.png" >}}' alt="" class="wp-image-492"/></figure>



<p><strong>Graph View.&nbsp;&nbsp;</strong>The Graph View provides analytics for a selected variable, time range, and a point or defined geographic area.&nbsp; &nbsp;Using the selections displayed on the left, the Graph view will plot the value of the selected variable for the selected temporal interval.&nbsp; If a point is selected, the graph view plots the value for the point. If a rectangle (or, later, other) area is selected, then the plot represents the average (mean) of the spatial cells within or overlapping the boundary.&nbsp; An uncertainty interval for the graph map be turned on or off. (Other ways of aggregating data for the selected area, and graph smoothing are under development.)</p>



<div class="wp-block-image"><figure class="alignright"><img src='{{< siteurl "wp-content/uploads/2018/06/Graph.png" >}}' alt="" class="wp-image-495"/></figure></div>



<p>Because graph generation is a computation-intensive procedure, it may take some time for the&nbsp;graph to be generated. The needed time will increase with the size of the geographic selection and the length of the temporal selection.&nbsp; If too large an area is selected, the server will time out.&nbsp; In that case a smaller area should be selected (options allowing longer computations will be added).&nbsp; No graph will be displayed before a variable and point or area have been selected.&nbsp; (Future versions will permit user-specified timouts.)</p>



<p>Tsde Download Chart button will download both the chart itself (in SVG format [other formats to come]) and the data underlying the graph in CSV format.</p>



<p>If the dataset does not represent a time series, the Graph View is grayed out and unavailable.</p>



<p><strong>Download.&nbsp;</strong> The download tab is under development but will allow the download (when permissible) of the geospatial source data for a variable, temporal, and geographic selection.</p>



<p><strong>Model.</strong>&nbsp;The Model tab is under development.&nbsp; When it is implement and when the model source code is available for the selected dataset, the model tab will allow "tinkering,"&nbsp; rerunning the model with different parameters.</p>



<p><strong>Help &amp; Comments. </strong>Please send comments and queries to <a href='mailto:kintigh@asu.edu'>Keith Kintigh</a>.</p>
