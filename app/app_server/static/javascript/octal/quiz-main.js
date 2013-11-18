/**
 * Main function, set to data-main with require.js
 */

// configure require.js
requirejs.config({
  baseUrl: window.STATIC_PATH + "javascript",
  paths: {
    jquery:"lib/jquery-2.0.3.min",
    underscore: "lib/underscore-min",
    backbone: "lib/backbone-min",
    d3: "lib/d3",
    "btouch": "lib/backbone.touch",
    "sidr": "lib/jquery.sidr.min"
  },
  shim: {
    d3: {
      exports: "d3"
    },
    underscore: {
      exports: "_"
    },
    backbone: {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    },
    "btouch": {
      deps: ["jquery", "underscore", "backbone"]
    },
    "sidr": ["jquery"]
  },
  waitSeconds: 15
});

/**
 * Handle uncaught require js errors -- this function is a last resort
 * TODO: anyway to reduce code repetition with other js files, considering the other js files won't be loaded?
 * perhaps define a global namespace of css classes and ids?
 */
if (window.PRODUCTION){
  requirejs.onError = function(err){
    var errorId = "error-message";
    if (document.getElementById(errorId) === null){
      var div = document.createElement("div");
      div.id = errorId;
      div.className = "app-error-wrapper"; // must also change in error-view.js
      div.textContent = "Sorry, it looks like we encountered a problem trying to " +
        "initialize the application. Refreshing your browser may solve the problem.";
      document.body.appendChild(div);
    }
    throw new Error(err.message);
  };
}

// agfk app & gen-utils
requirejs(["backbone", "octal/routers/quiz-router", "jquery", "btouch", "sidr"], function(Backbone,  QuizRouter, $, GenPageUtils, AuxModel ){
  "use strict";

  
  // shim for CSRF token integration with backbone and django
  var oldSync = Backbone.sync;
  Backbone.sync = function(method, model, options){
    options.beforeSend = function(xhr){
      if (model.get("useCsrf")){
        xhr.setRequestHeader('X-CSRFToken', window.CSRF_TOKEN);
      }
    };
    return oldSync(method, model, options);
  };
  
  //GenPageUtils.prep();

  // automatically resize window when viewport changes
  //Utils.scaleWindowSize("header", "main");

  $("body").on("mousedown", ".external-link", function(evt){
    if(window._paq){
      window._paq.push(['trackLink', evt.currentTarget.href, "link"]);
    }
  });
  $(window).on("hashchange", function() {
    if(window._paq){
      window._paq.push(['trackPageView', window.location.hash]);
    }
  });

  // start the AGFK app
  var quizRouter = new QuizRouter();
  Backbone.history.start();
});
