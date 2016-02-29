'use strict';

var appControllers = angular.module('centrakControllers', []);
appControllers.controller('CaptureViewCtrl', function($scope, $http, $compile){
	// global variables
	$scope._local_scopes = {};
	$scope._choices = null;
	$scope._meta = null;
	
	$scope.paneSetup = function() {
		// bind to duplicate controls
		var controls = angular.element('.side-dash .identical-entries .item');
		angular.forEach(controls, function(value, key) {
			angular.element(value).on('change', function() {
				var control = value.children[0].children[0]
				  , id = control.getAttribute('value')
				  , captureType = control.getAttribute('data-type');
				if (id === '') {
					var out = angular.element('.r-view')
					  , scope = $scope._local_scopes['extra'];
					
					if (scope !== null && scope !== undefined) {
						$scope._local_scopes['extra'] = null;
						scope.capture = null;
						scope.$destroy();
					}
				
					out.empty();
					return;
				} else {
					$scope.displayCapture(id, false, captureType);
					return true;
				}
			});
		});		
		
		// next controls
	};

	// functions...
	$scope.displayCapture = function(captureId, isFirst, captureType) {
		// pull capture from server
		var urlpath = $scope._getUrl(captureId, isFirst, captureType);
		$http({'method':'GET', 'url':urlpath})
			.then(function success(resp) {
					  if (isFirst) {
						  $scope._choices = resp.data._choices;
						  $scope._meta = resp.data._meta;
					  }
					  var capture = resp.data.capture;
					  $scope.showInForm(capture, isFirst, captureType);
				  },
				  function failed(resp) {
					  alert(resp.data.toString());
					  return true;
				  });
	};
		
	$scope.showInForm = function(capture, isFirst, captureType) {
		var snippet = angular.element('#capture_snippet')
		  , view = angular.element(isFirst? '.l-view': '.r-view')
		  , form = angular.element(snippet.html())
		  , scope = $scope.$new(true);
		
		scope._choices = $scope._choices;
		scope._meta = $scope._meta;
		scope.capture = capture;
		scope.prefix = (new Date().getTime() % 100000);
		
		// modify form
		form.find('.section-head').text(
			(isFirst? 'Capture': captureType) + ' Entry');
		
		if (!isFirst) {
			form.addClass('bg-warn');
			form.find('.panel')
				.removeClass('panel-default')
				.addClass('panel-warning');			
		}
		
		var new_form = $compile(form)(scope)
		  , btn = new_form.find('[name=save]')
		  , key = isFirst? 'main': 'extra';
				
		btn.on('click', $scope.updateCapture);
		btn.data('scope-key', key);
		
		$scope._local_scopes[key] = scope;
		view.empty().append(new_form);
	};
	
	$scope.updateCapture = function(e) {
		var key = angular.element(e.currentTarget).data('scope-key')
		  , scope = $scope._local_scopes[key];
		
		if (key !== 'main') {
			alert('Updating duplicate or update captures not supported.')
			return false;
		}
				
		if (scope !== null) {
			var data = {'capture': scope.capture}
			  , urlpath = '/api' + window.location.pathname + 'update';
				  
			$http({'method':'POST', 'data':data, 'url':urlpath})
				.then(function success(resp) {
						  alert(resp.data.message);
					  },
					  function failure(resp) {
						  alert(resp.data.toString());
					  });
		}
		else
			alert('could not retrieve capture');
	};
	
	$scope._getUrl = function(captureId, isFirst, captureType) {
		var source = (captureType === 'duplicate'
						? $scope.recordType
						: $scope.recordType === 'captures' 
							? 'updates' : 'captures');
		
		if (isFirst)
			return '/api' + window.location.pathname;
		
		return ('/api/' + source + '/' + captureId + '/?record_only=true');
	}
		
	angular.element(document).ready(function(){
		var urlpaths = window.location.pathname.split('/')
		  , captureId = urlpaths[2];
		
		// bind pane controls
		$scope.paneSetup();
		
		// display capture
		$scope.recordType = urlpaths[1];
		$scope.displayCapture(captureId, true);
	});
})

