<div class="x">
    <form method="post" class="form-horizontal form-compressed">
        <div class="panel-group" id="accordion_{{title}}">
        % for index, title in enumerate(form._meta['fields']):
            % fieldset = form._meta['fields'][title]
            <div class="panel panel-default panel-compressed">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a role="button" data-toggle="collapse" data-parent="#accordion_{{title}}" href="#collapse_{{title}}">
                            {{ title }}
                        </a>
                    </h4>
                </div>
                % if index > 0:
                <div id="collapse_{{title}}" class="panel-collapse collapse">
                % end
                    <div class="panel-body">
                        % for field in fieldset:
                        <div class="form-group">
                            <label for="id_{{field}}" class="col-md-3 control-label">{{ fieldset[field] }} : </label>
                            <div class="col-md-8">
                                {{! form.render_field(field, record) }}
                            </div>
                        </div>
                        % end
                    </div>
                % if index > 0:
                </div>
                % end
            </div>
        % end
        </div>
    </form>
</div>