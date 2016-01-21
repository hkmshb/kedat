 <div class="row">
    <div class="col-md-9">
      <form method="post">
        <div class="panel panel-default">
            <div class="panel-heading">
                {{ title }} / <b>{{ xform.title }}</b>
            </div>
            <div class="panel-body">
                <table border="0" class="table panel-table table-figures">
                    <thead>
                        <tr class="group-desc">
                            <th></th><th ></th>
                            <th colspan="2" class="lvsep col-shade">Duplicates</th>
                            <th colspan="4" class="lvsep">Account Status</th>
                            <th colspan="3" class="lvsep col-shade">Meter Type</th>
                        </tr>
                        <tr><th>&nbsp;</th>
                            <th class="lvsep">Total</th>
                            <th class="col-shade lvsep">#RS</th>
                            <th class="col-shade">#AC</th>

                            <th title="# New" class="lvsep">#.N</th>
                            <th title="# Active">#.A</th>
                            <th title="# Inactive">#.I</th>
                            <th title="# Unknown">#.U</th>

                            <th title="# Analogue" class="col-shade lvsep">#.Alog</th>
                            <th title="# PPM" class="col-shade">#.PPM</th>
                            <th title="# None" class="col-shade">#.NA</th>
                        </tr>
                    </thead>
                    <tbody>
                    % if records:
                        % for r in records:
                        <tr><td>{{ r.date }}</td>
                            <td class="lvsep">{{ r._total }}</td>

                            <td class="col-shade lvsep">{{ r._rseq_duplicates }}</td>
                            <td class="col-shade">{{ r._acctno_duplicates }}</td>
                            
                            <td class="lvsep">{{ r.new }}</td>
                            <td>{{ r.active }}</td>
                            <td>{{ r.inactive }}</td>
                            <td>{{ r.unknown }}</td>

                            <td class="col-shade lvsep">{{ r.analogue }}</td>
                            <td class="col-shade">{{ r.ppm }}</td>
                            <td class="col-shade">{{ r.none }}</td>
                        </tr>
                        % end
                    % else:
                        <tr><td>No data available.</td></tr>
                    % end
                    </tbody>
                </table>
            </div>
        </div>
      </form>
    </div>

    <div class="col-md-3">
        % include('calendar.tpl')
        
        <div class="clearfix">&nbsp;</div>
        <div style="padding-top:10px;">
            <div class="panel panel-info">
                <div class="panel-heading">Sync History</div>
                <div class="panel-body">
                    <form method="post" class="form-inline">
                        <div class="form-group">
                            <div class="input-group date">
                                <input type="text" class="form-control" 
                                       placeholder="dd/mm/yyyy" required disabled>
                                    <span class="input-group-addon"><i class="glyphicon glyphicon-th"></i></span>
                                </input>
                            </div>
                        </div>
                        <input type="hidden" name="sync_date" value="" />
                        <input type="hidden" name="id_string" value="{{ xform.id_string }}" />
                        <button type="submit" class="btn btn-primary">Sync</button>
                    </form>
                    <hr style="margin-bottom:10px;"/>

                    <table class="table table-condensed panel-table">
                        <tbody>
                        % if not sync_records:
                            <tr><td><span class="text-info" title="Date Performed">2016-01-11</span> / 
                                    <span title="Date Entered">2016-01-11</span>
                                </td>
                                <td title="Quantity Synced">300</td></tr>
                        % else:
                            <tr><td>No data available.</td></tr>
                        % end
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </div>
 </div> 

 % def script():
    <script type="text/javascript">
        (function($){
            $(function(){
                $('.input-group.date').datepicker({
                        format: "dd/mm/yyyy", clearBtn: true,
                        autoclose: true, toggleActive: true,
                        todayHighlight: true,
                    }).on('clearDate', function(e) {
                        $('[name=sync_date]').val('');
                    }).on('changeDate', function(e) {
                        $('[name=sync_date]').val(e.format('yyyy-mm-dd'));
                    });
            });
        })(jQuery);
    </script>
 % end

 % rebase('layout.tpl', title=title, year=year, extra_scripts=script)
