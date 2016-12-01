


var app = angular.module('peopleApiApp', []);

app.controller('peopleApiCtrl', ['$scope', '$http',
	function($scope, $http){



		// INITIATLIZE VARIABLES ON LOAD

		$scope.init = function(){

			$scope.people = [
				"Dawson Spencer",
				"Rob Korobkin",
				"Simon Hergenhan",
				"Adam Gilman",
				"banana"
			];


		}


		// MAKE API CALL AND LOAD RETURNED JSON
		$scope.fetchPerson = function(){

			var req = {
				verb : 'getPerson',
				name : $scope.selectedName
			}

			$http.post('api.py', req).then(function(response){
				$scope.selected_person = response.data;
			});		
		}

		$scope.init();

}]);


