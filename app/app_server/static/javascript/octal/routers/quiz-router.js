define(["backbone", "jquery", "octal/models/quiz-model", "octal/views/quiz-view"], function(Backbone, $, QuestionModel, QuizView) {
    var pvt = {
				qviewId: "quiz-wrapper"
		};
		return QuizRouter = Backbone.Router.extend({
        initialize: function() {
				},
				
				routes: {
						"":"showError",
						"concept/:concept": "showQuiz",
						"about" : "showAbout"
				},
				
				showError: function() {
					  console.log("you must specify a concept");
				},

				showQuiz: function(concept) {
            var thisRoute = this,
						qviewId = pvt.qViewId;
						console.log("you have selected the concept: " + concept);
						var questionModel = new QuestionModel();
						thisRoute.qview = new QuizView({model: questionModel});
						thisRoute.qview.render();
						$("#quiz-wrapper").html(thisRoute.qview.$el).show();
				}
		});

});