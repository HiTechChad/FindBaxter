var app = angular.module('peopleApiApp', []);

app.controller('peopleApiCtrl', ['$scope', '$http',
	function($scope, $http){

		window.$scope = $scope;

		// INITIATLIZE VARIABLES ON LOAD

		$scope.init = function(){
			$scope.people = [
				"Dawson Spencer",
				"Rob Korobkin",
				"Simon Hergenhan",
				"Adam Gilman",
				"banana"
			];
			$scope.meetings = [
				"short",
				"meadium",
				"long"
			
			];
			$scope.newPerson = {
				name : "",
				email : "",
			}
			$scope.fetchEveryone();


			$scope.all_users = [];
			if('all_users' in staticData){
				$scope.all_users = staticData.all_users;
			}
		}


		// CHANGE VIEW
		$scope.changeView = function(viewName){
			$scope.view = viewName;
		}



		/*********************************************************
		* API INTEGRATION
		**********************************************************/

		// CALL API
		$scope.callAPI = function(req, f){
			$http.post('api.py', req).then(function(responseHTTP){
				var response = responseHTTP.data;
				if(("error" in response)) {
					$scope.view = 'error';
					$scope.error = response.error;
				}
				else f(response);
			});
		}


		// FETCH PERSON BY NAME
		$scope.fetchPerson = function(){
			var req = {
				verb : 'getPerson',
				name : $scope.selectedName
			}

			$scope.callAPI(req, function(response){
				$scope.selected_person = response;
				$scope.view = 'viewPerson'
			});		
		}
		
		// Fetch Everyone by name
		$scope.fetchEveryone = function(){
			var req = {
				verb: 'getPeople'
			}
			
			$scope.callAPI(req, function(response){
				$scope.all_users = response;
				$scope.view = 'viewPerson'
			});
		}
		
		//MEETING REQUEST
		$scope.ReqMeeting = function(){
			var req = {
				verb:'sendTxt',
				name: $scope.reqName
			}
			$scope.callAPI(req, function(){
				$scope.number = response;
				$scope.view = 'viewPerson'
			});
		}
		
		// ADD PERSON
		$scope.addPerson = function(){

			// VALIDATION
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


			// API CALL
			var req = {
				verb : 'addPerson',
				person : $scope.newPerson
			}
			$scope.callAPI(req, function(response){
				$scope.selected_person = $scope.newPerson;
				$scope.view = 'viewPerson';
				$scope.people.push($scope.newPerson.name)
			});		
		}
		

		// INIT AND LAUNCH APP
		$scope.init();


}]);

function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}


