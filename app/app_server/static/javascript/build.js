({
  baseUrl: ".",
  name: "agfk/main.js",
  out: "agfk/main-built.js",
  paths: {
    jquery:"lib/jquery-2.0.3.min",
    "jquery.cookie": "lib/jquery.cookie",
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
    "jquery.cookie"  : {
      deps: ["jquery"]
    },
    "btouch" : {
      deps: ["jquery", "underscore", "backbone"]
    },
    "sidr": ["jquery"]
  }
})
