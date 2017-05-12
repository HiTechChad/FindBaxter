


var app = angular.module('selectorApp', []);

app.controller('selectorCtrl', ['$scope', 
	function($scope){


		$scope.person = {
			name : "What is your name?"
		}


		$scope.changeName = function(){
			$scope.person.name = 'Dawson'
		}



}]);


