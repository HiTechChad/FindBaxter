var app = angular.module('peopleApiApp', []);

app.controller('peopleApiCtrl', ['$scope', '$http',
	function($scope, $http){

		window.$scope = $scope;

		// INITIATLIZE VARIABLES ON LOAD

		$scope.init = function(){
			$scope.login();
			
		}
		$scope.telephone

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
					if(response.error == "No Access Token" || response.error =="Bad Token" || response.error == "Bad Google Token"){
						window.location.replace('http://localhost:8888/login.html');

					}
					$scope.view = 'error';
					$scope.error = response.error;
				}
				else f(response);
			});
		}
		// LOGIN
		$scope.login = function(){
			var req = {
				verb : 'login',
				google_token : localStorage.getItem("google_token")
			}
			var callback = function(response){
				localStorage.setItem("access_token", response.response);
				$scope.access_token = response.response;
				$scope.user = response.user;
				
				if($scope.user.telephone != null || $scope.user.telephone != ""){
					$scope.fetchEveryone();
				}else if($scope.user.telephone == null || $scope.user.telephone == ""){
					$scope.view = "verifyTelephone"
				}
			}
			$scope.callAPI(req, callback);
		}

		// FETCH PERSON BY NAME
		$scope.fetchPerson = function(){
			var req = {
				verb : 'getPerson',
				name : $scope.selectedName,
				access_token: localStorage.getItem("access_token")
			}

			$scope.callAPI(req, function(response){
				$scope.selected_person = response;
				$scope.view = 'viewPerson';
			});		
		}
		
		// Fetch Everyone by name
		$scope.fetchEveryone = function(){
			var req = {
				verb: 'getPeople',
				access_token: localStorage.getItem("access_token")
			}
			
			$scope.callAPI(req, function(response){
				$scope.all_users = response;
				$scope.view = 'list';
			});
		}
		
		//MEETING REQUEST
		$scope.ReqMeeting = function(username, meeting){
			var req = {
				verb:'SendMessage',
				username: $scope.user.name,
				name: username,
				meeting: meeting,
				access_token: localStorage.getItem("access_token")
			}
			var callback = function(response){
				$scope.toUser = response;
				$scope.view = 'request';
				document.getElementById("messageDetails").style.display = null;
				document.getElementById("messageDetails").style.visibility = "visible";
				document.getElementById("table").style.display = "none";
			}
			$scope.callAPI(req, callback);
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
function closeConfermation(){
	document.getElementById("messageDetails").style.display = "none";
	document.getElementById("messageDetails").style.visibility = "hidden";
	document.getElementById("table").style.display = null;
}
