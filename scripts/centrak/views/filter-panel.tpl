% get = lambda x: x['$regex'][2:-2] or '' if x else ''
% selected = lambda x, y: 'selected=""' if x and (x['$regex'][2:-2] or '') == y else ''
<form class="form-stacked" method="get">
    <div class="filter-panel">
        <a href="javascript:;" data-click="filter-panel-expand" class="filter-collapse-btn">
            <i class="glyphicon glyphicon-filter"></i>
        </a>
        <div class="filter-panel-content">
            <h5 class="m-t-0">Filter Parameters</h5>
            <div class="divider"></div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Capture Date</div>
                <div class="col-md-7">
                    <div class="input-group date">
                        <input type="text" class="form-control" name="datetime_today" placeholder="yyyy-mm-dd" 
                               value="{{ get(q.datetime_today) }}" required="" disabled="">
                            <span class="input-group-addon btn" style="border-radius: 0 4px 4px 0;">
                                <i class="glyphicon glyphicon-th"></i>
                            </span>
                        </input>
                    </div>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Enumerator ID</div>
                <div class="col-md-7">
                    <input type="text" class="form-control" name="enum_id" value="{{ get(q.enum_id)}}"/>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Route Sequence</div>
                <div class="col-md-7">
                    <input type="text" class="form-control" name="rseq" value="{{ get(q.rseq) }}" />
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Account Status</div>
                <div class="col-md-7">
                    <select name="acct_status" class="form-control input-sm">
                        <option value="">&lt;Select One&gt;</option>
                    % for item in acct_status_choices:
                        <option value="{{ item[0] }}" {{ selected(q.acct_status, item[0]) }}>{{ item[1] }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Book Code</div>
                <div class="col-md-7">
                    <input type="text" class="form-control input-sm" name="book_code" 
                           value="{{ get(q.acct_no) }}" />
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Meter Status</div>
                <div class="col-md-7">
                    <select name="meter_status" class="form-control input-sm" placeholder="Select Meter Status">
                        <option value="">&lt;Select One&gt;</option>
                    % for item in meter_status_choices:
                        <option value="{{ item[0] }}" {{ selected(q.meter_status, item[0]) }}>{{ item[1] }}</option>
                    % end
                    </select>
                </div>
            </div>
            <div class="row m-t-10">
                <div class="col-md-5 control-label">Meter Type</div>
                <div class="col-md-7">
                    <select name="meter_type" class="form-control input-sm">
                        <option value="">&lt;Select One&gt;</option>
                    % for item in meter_type_choices:
                        <option value="{{ item[0] }}" {{ selected(q.meter_type, item[0]) }}>{{ item[1] }}</option>
                    % end
                    </select>
                </div>
            </div>

            <div class="row m-t-10">
                <div class="col-md-12">
                    <button type="submit" class="btn btn-default" name="filter">Filter</button>
                    <button type="reset" class="btn btn-default" name="reset">Clear</button>
                </div>
            </div>
        </div>
    </div>
</form>