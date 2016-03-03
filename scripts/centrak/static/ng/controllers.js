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
		scope.onRSeqChanged = handleRSeqChanged(scope);
		
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
		  , btnExpand = new_form.find('[name=expand]')
		  , btnSave = new_form.find('[name=save]')
		  , key = isFirst? 'main': 'extra';
		
		btnExpand.on('click', togglePanes($(btnExpand).find('i'), new_form));
		btnSave.on('click', $scope.updateCapture);
		btnSave.data('scope-key', key);
		
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
			
			// validate route sequence
			if (!isValidRouteSeqFormat(scope.capture.rseq)) {
				alert('Capture route sequence format is invalid.')
				return false;
			}
			
			// validate acct number
			if (scope.capture.acct_no && scope.capture.acct_no.length > 1) {
				if (!isValidAcctNoFormat(scope.capture.acct_no)) {
					alert('Capture account number is format is invalid.')
					return false;
				}
			}
			
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
	

	var isValidRouteSeqFormat = function(value) {
		if (value && value.length === 13) {
			var parts = value.split('/');
			if (parts.length === 3) {
				var sscode=parts[0].toUpperCase() 
				  , upcode=Number(parts[1])
				  , sn=Number(parts[2]);
				
				if (sscode.length !== 6 || parts[1].length !== 1 || parts[2].length !== 4 ||
					isNaN(Number('0x' + sscode.substring(2))))
					return false;
				
				if (sscode[0] !== 'S' || (sscode[1] !== '1' && sscode[1] !== '3'))
					return false;
				
				if (isNaN(upcode) || upcode < 0 || upcode > 4)
					return false;
				
				if (isNaN(sn)) 
					return false;
				return true;
			}
		}
		return false;
	},
	isValidAcctNoFormat = function(value) {
		if (value && value.length == 16) {
			var parts = value.split('/');
			if (parts.length == 4) {
				var i, part, no=parts[3];
				for (i==0; i < 2; i++) {
					part = parts[i];
					if (part.length !== 2 || isNaN(Number(part))) 
						return false;
				}
				
				if (no.length !== 7 || no.indexOf('-01') !== 4 ||
					isNaN(Number(no.substring(0, 4))))
					return false;
				return true;
			}
		}
		return false;
	},
	handleRSeqChanged = function(scope) { 
		return function(newValue, oldValue) {
			if (!isValidRouteSeqFormat(newValue))
				return;
			
			var parts = newValue.toUpperCase().split('/');
			scope.capture.station = parts[0];
			scope.capture.upriser = parts[0] + "/" + parts[1];
		}
	},
	togglePanes = function(icon, form) {
		return function() {
			var panes = form.find('.panel-collapse')
			  , pane = angular.element(panes[1])
			  , isCollapsed = pane.hasClass('collapse');
			
			if (isCollapsed)
				icon.removeClass('glyphicon-resize-full')
					.addClass('glyphicon-resize-small');
			else
				icon.removeClass('glyphicon-resize-small')
					.addClass('glyphicon-resize-full');
				
			for (var i=1; i < panes.length; i++) {
				pane = angular.element(panes[i]);
				if (isCollapsed)
					pane.removeClass('collapse').removeClass('in');
				else
					pane.addClass('collapse');
			}
		}
	};
})

