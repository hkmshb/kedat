<div class="row" ng-controller="CaptureListCtrl">
    <div class="col-md-6">
        <h5 style="text-transform:uppercase; font-weight:bold;">Capture Entry</h5>
        %include('capture_snippet.tpl', record=record)
    </div>
</div>

% def scripts():
    <script src="/static/ng/angular.min.js"></script>
    <script src="/static/ng/app.js"></script>
    <script src="/static/ng/controllers.js"></script>
    <script src="/static/ng/directives.js"></script>
% end
% rebase('layout.tpl', title=title, year=year, extra_scripts=scripts)
