

/* START ANGULAR APP */
var app = angular.module('selectorApp', []);
app.controller('selectorCtrl', ['$scope', 
	function($scope){



		/* EXAMPLE CODE */

		$scope.person = {
			name : "What is your name?"
		}

		$scope.changeName = function(){
			$scope.person.name = 'Dawson'
		}



}]);


