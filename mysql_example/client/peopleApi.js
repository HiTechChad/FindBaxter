


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
			console.log("hurray");
			var req = {
				verb : 'getPerson',
				name : $scope.selectedName
			}

			$http.post('api.py', req).then(function(response){
				$scope.selected_person = response.data;
			});		
		}
		$scope.init();

		$scope.test = function(){
			console.log("got this far");
			var reqs = {
				verb : 'addPerson',
				name : $scope.personAdd
			}
			$http.post('api.py', reqs).then(function(response){
				console.log("added");
			});
		}
		
		$scope.init();


}]);


