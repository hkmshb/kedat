'use strict';

var appControllers = angular.module('centrakControllers', []);

appControllers.controller('CaptureListCtrl', function($scope, $http) {
	$scope.captureId = null;
	$scope.capture = null;
	$scope._choices = null;
	$scope._meta = null;
	$scope.failed = false;
	$scope.rendered = [];
	
	angular.element(document).ready(function(){
		$scope.init();
	})	
	
	$scope.init = function() {
		var captureId = location.pathname.split('/')[2];
        $scope.listCaptures(captureId);
		$scope.captureId = captureId;
	};
	
	$scope.listCaptures = function(captureId) {
        var url = '/api/captures/' + captureId + '/';
        
		$http({'method':'GET', 'url':url})
			.then(function successCallback(resp) {
					$scope.capture = resp.data.capture;
					$scope._meta = resp.data._meta;
					$scope._choices = resp.data._choices;
					return true;
				 },
				 function errorCallback(resp) {
					alert(resp.data.toString());
					return true;
				 });
	};
	
	$scope.listenForChange = function(nval, oval) {
		if (nval.trim().length != 12) {
			alert("Invalid route sequence provided");
			$scope.capture.rseq = oval;
		}
		
	}

});