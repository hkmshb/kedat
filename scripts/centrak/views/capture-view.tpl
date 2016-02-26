<div class="row" ng-controller="CaptureListCtrl" style="min-height: 500px;">
    <div class="col-md-2 affix side-dash" style="padding-right: 30px">
        <h5 style="text-transform:uppercase; font-weight:bold;"> &nbsp; </h5>
        <div class="panel panel-default panel-compressed">
            <div class="panel-body">
                <div class="panel-section section">
                    <h6>Duplicates</h6>
                    <ul class="duplicates">
                    % if duplicates:
                        <li class="item">
                            <label for="id_clear">
                                <input type="radio" id="id_clear" name="duplicate" value="" /> Clear Selection
                            </label>
                        </li>
                        % for d in duplicates:
                        <li class="item">
                            <label for="id_{{ d._id }}">
                                <input type="radio" id="id_{{ d._id }}" name="duplicate" value="{{ d._id }}" /> {{ d.rseq }} 
                            </label>
                        </li>
                        % end
                    % else:
                        <li>None Found</li>
                    % end
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-5 col-md-offset-2">
        <h5 class="section-head">Capture Entry</h5>
        <div ng-include="'capture_snippet'" ng-cloak></div>
    </div>
    <div class="col-md-5 compared-item">
        &nbsp;
    </div>
</div>

% def scripts():
    <script src="/static/ng/angular.min.js"></script>
    <script src="/static/ng/app.js"></script>
    <script src="/static/ng/controllers.js"></script>
    <script src="/static/ng/directives.js"></script>
    
    <!-- script template -->
    <script type="text/ng-template" id="capture_snippet">
      <div class="capture_form">
        <form method="post" class="form-horizontal form-compressed">
            <div class="panel-group" id="accordion_:{ title }:">
                <div class="panel panel-default panel-compressed" ng-repeat="(title, meta) in _meta.fields">
                    <div class="panel-heading" ng-if="title !== 'capture'">
                        <h4 class="panel-title">
                            <a role="button" data-toggle="collapse" data-parent="#accordion_:{ title }:" href=".collapse_:{ title }:"
                               ng-click="toggle_pane(title)">
                                :{ title }:
                            </a>
                        </h4>
                    </div>
                    <div class="collapse_:{ title }: panel-collapse" ng-class="{'collapse': title !== 'capture'}">
                        <div class="panel-body">
                            <div class="form-group" ng-repeat="(field, label) in meta">
                                <label for="id_:{field}:" class="col-md-4 control-label">:{ label }:: </label>
                                
                                <div class="col-md-8" ng-if="field[0] == '_' || title == 'meta'">
                                    <label ng-if="title != 'meta'" id="id_:{ field }:" name=":{ field }:" class="form-control-static">:{ capture[field.substr(1)] }:</label>
                                    <label ng-if="title == 'meta'" id="id_:{ field }:" name=":{ field }:" class="form-control-static">:{ capture[field] }:</label>
                                </div>
                                
                                <div class="col-md-8" ng-if="_meta.widgets.select.indexOf(field) > -1">
                                    <select id="id_:{ field }:" name=":{ field }:" class="form-control" >
                                        <option value="">&laquo; Select One &raquo;</option>
                                        <option ng-repeat="(value, text) in _choices[field]" value=":{ value }:"
                                                ng-selected="capture[field] == value">:{ text }:</option>
                                    </select>
                                </div>
                                
                                <div class="col-md-8" ng-if="field[0] !== '_' && title !== 'meta' && _meta.widgets.select.indexOf(field) == -1">
                                    <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                           change-on-blur="listenForChange(newValue, oldValue)"
                                           ng-if="field === 'rseq'" />
                                    <input type="text" id="id_:{ field }:" name=":{ field }:" class="form-control" ng-model="capture[field]"
                                           ng-if="field !== 'rseq'" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
      </div>
    </script>
    
% end
% rebase('layout.tpl', title=title, year=year, extra_scripts=scripts)
