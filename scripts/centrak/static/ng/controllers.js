'use strict';

var appControllers = angular.module('centrakControllers', []);
appControllers.controller('CaptureViewCtrl', function($scope, $http, $compile){
	// global variables
	$scope._coll = new Collection();
	$scope._choices = null;
	$scope._meta = null;
	
	$scope.changeSelection = function() {
		
	};
	
	$scope.paneSetup = function() {
		// bind to duplicate controls
		var controls = angular.element('.side-dash .duplicates .item');
		angular.forEach(controls, function(value, key) {
			angular.element(value).on('change', function() {
				var id = value.children[0].children[0]['value'];
				if (id === '') {
					var out = angular.element('.r-view')
					  , local_scope = out.data('local-scope');
					
					if (local_scope !== null)
						local_scope.$destroy();
				
					out.empty();
					return;
				} else {
					$scope.displayCapture(id, false);
					return true;
				}
			});
		});		
		
		// next controls
	};

	// functions...
	$scope.displayCapture = function(captureId, isFirst) {
		if (!$scope._coll.hasId(captureId)) {
			// pull capture from server
			var urlpath = (isFirst
				? '/api' + window.location.pathname
				: '/api/' + $scope.recordType + '/' + captureId + '/?record_only=true');
			
			$http({'method':'GET', 'url':urlpath})
				.then(function success(resp) {
						  if (isFirst) {
							  $scope._choices = resp.data._choices;
							  $scope._meta = resp.data._meta;
						  }
						  var capture = resp.data.capture;
						  $scope._coll.add(capture);
						  $scope.showInForm(capture, isFirst);
					  },
					  function failed(resp) {
						  alert(resp.data.toString());
						  return true;
					  });
		} else {
			var capture = $scope._coll.get(captureId);
			if (capture !== null)
				$scope.showInForm(capture, isFirst);
		}
	};
		
	$scope.showInForm = function(capture, isFirst) {
		var coll = $scope._coll
		  , snippet = angular.element('#capture_snippet')
		  , view = angular.element(isFirst? '.l-view': '.r-view')
		  , form = angular.element(snippet.html())
		  , scope = $scope.$new(true);
		
		scope._choices = $scope._choices;
		scope._meta = $scope._meta;
		scope.capture = capture;
		scope.prefix = (new Date().getTime()/100000);
		
		form.find('.section-head').text(
			(isFirst? 'Capture': 'Duplicate') + ' Entry');
		
		if (!isFirst) {
			form.addClass('bg-warn');
			form.find('.panel')
				.removeClass('panel-default')
				.addClass('panel-warning');
		}
		
		var xml = $compile(form)(scope)
		  , btn = xml.find('[name=save]');
		
		btn.data('capture-id', capture._id)
		btn.on('click', $scope.updateCapture);
		
		view.empty().append(xml);
		view.data('local-scope', scope);
	};
	
	$scope.updateCapture = function(e) {
		var captureId = angular.element(e.currentTarget).data('capture-id')
		  , capture = $scope._coll.get(captureId);
		
		if (capture !== null)
			return alert(capture.cust_name);
		else
			return alert('could not retrieve capture');
	};
		
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



var Collection = function() {
	var coll = [];
	
	this.add = function(element) {
		if (element !== null && element !== undefined) {
			coll.push(element);
		}
	};
	
	this.get = function(id) {
		for (var i in coll) {
			if (coll[i]._id.toString() === id.toString())
				return coll[i]
		}
		return null;
	};
	
	this.has = function(elem) {
		for (var i in coll) {
			if (coll[i]._id.toString() === elem._id.toString())
				return true;
		}
		return false;
	};
	
	this.hasId = function(id) {
		for (var i in coll) {
			if (coll[i]._id.toString() === id.toString())
				return true;
		}
		return false;
	}
}

