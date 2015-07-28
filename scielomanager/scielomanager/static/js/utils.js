/*
 * Use utils.js for generic functions to support javascripts to the application
 *
 */

function updateQueryStringParameter(uri, key, value) {
  // Function to add any value to query string

  var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  var separator = uri.indexOf('?') !== -1 ? "&" : "?";

  if (uri.match(re)) {
    return uri.replace(re, '$1' + key + "=" + value + '$2');
  }
  else {
    return uri + separator + key + "=" + value;
  }

}