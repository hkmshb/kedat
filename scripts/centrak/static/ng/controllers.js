'use strict';

var appControllers = angular.module('centrakControllers', []);

appControllers.controller('CaptureListCtrl', function($scope, $http, $compile) {
	$scope.capture = null;
	$scope._choices = null;
	$scope._meta = null;
	$scope.failed = false;
	$scope.rendered = [];
	
	angular.element(document).ready(function(){
		$scope.init();
		$scope.bindToDash();
	})	
	
	$scope.init = function() {
		var captureId = location.pathname.split('/')[2];
        $scope.listCaptures();
	};
	
	$scope.listCaptures = function(captureId) {
        var url = '/api' + window.location.pathname
          , record_type = window.location.pathname.split('/')[1];
        
        $scope.record_type = record_type;
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
	
	$scope.bindToDash = function() {
		var items = angular.element('.side-dash .duplicates .item')
		  , url = '/api/' + $scope.record_type + '/';
		
		angular.forEach(items, function(value, key){
			angular.element(value).on('change', function(){
				var id = value.children[0].children[0]['value'];
				if (id === "") {
					var out = angular.element('.compared-item');
					out.html('');
					return;
				}
				
				$http({'method':'GET', 'url': url + id + '/?record_only=true'})
					.then(function success(resp) {
						var tpl = angular.element('#capture_snippet')
						  , out = angular.element('.compared-item')
						  , local_scope = $scope.$new(true);
						
						local_scope.capture = resp.data.capture;
						local_scope._meta = $scope._meta;
						local_scope._choices = $scope._choices;
						
						out.html('<h5 class="section-head">Duplicate Entry</h5>');
						var xml = $compile(tpl.html())(local_scope);
						out.append(xml);
					});
			});
		});
	}
});
