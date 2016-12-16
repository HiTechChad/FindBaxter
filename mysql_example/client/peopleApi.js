


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
			$scope.newPerson = {
				name : "",
				email : ""
			}
		}

		// CHANGE VIEW
		$scope.changeView = function(viewName){
			$scope.view = viewName;
		}


		// MAKE API CALL AND LOAD RETURNED JSON
		$scope.fetchPerson = function(){
			var req = {
				verb : 'getPerson',
				name : $scope.selectedName
			}

			$http.post('api.py', req).then(function(response){
				$scope.selected_person = response.data;
				$scope.view = 'viewPerson'
			});		
		}

		$scope.addPerson = function(){

			$scope.errors = {};

			if($scope.newPerson.name == ""){
				$scope.errors.name = true;
			}

			if($scope.newPerson.email == ""){
				$scope.errors.email = true;
			}

			if(!isEmail($scope.newPerson.email)){
				$scope.errors.email = true;
				$scope.errors.badEmail = true;
			}			

			if(!$.isEmptyObject($scope.errors)) return;

			var req = {
				verb : 'addPerson',
				person : $scope.newPerson
			}
			$http.post('api.py', req).then(function(responseHTTP){
				var response = responseHTTP.data;
				if(!("error" in response)) {
					$scope.selected_person = $scope.newPerson;
					$scope.view = 'viewPerson';
					$scope.people.push($scope.newPerson.name)
				}
			});
		}
		
		$scope.init();


}]);

function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}


