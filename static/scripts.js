
// execute when the DOM is fully loaded


$(document).ready(function(){
  // we call the function
  configure();
});

/**
 * Configures application.
 */
function configure()
{
    // configure typeahead
    $("#q").typeahead({
        highlight: false,
        minLength: 1
    },
    {
        display: function(suggestion) { return null; },
        limit: 10,
        source: search,
        templates: {
            suggestion: Handlebars.compile(
                "<div id='suggestion'>" +
                "{{title}} " +
                "</div>"
            )
        }
    });

    // re-center map after place is selected from drop-down
    $("#q").on("typeahead:selected", function(eventObject, suggestion, name) {
        window.location.href = "/recipe?id=" + (suggestion.id_r);


    });

    // hide info window when text box has focus
    $("#q").focus(function(eventData) {
        info.close();
    });


    // give focus to text box
    $("#q").focus();
}



/**
 * Searches database for typeahead's suggestions.
 */
function search(query, syncResults, asyncResults)
{
    // get places matching query (asynchronously)
    var parameters = {
        q: query
    };
    $.getJSON(Flask.url_for("search"), parameters)
    .done(function(data, textStatus, jqXHR) {

        // call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {

        // log error to browser's console
        console.log(errorThrown.toString());

        // call typeahead's callback with no results
        asyncResults([]);
    });
}


