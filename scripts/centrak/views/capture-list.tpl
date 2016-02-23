% f = lambda x: x or '-'
% enum = lambda x: '%s<b> / </b>%s' % (x[0], x[2:].title())
% addy = lambda x: '' if x.upper() in ['NA','N/A'] else x
% shorten = lambda x: x if x=='-' or len(x) < 22 else x[:22]+'...'

<div class="form-search">
    <div class="row">
        <div class="col-md-8"><span class="h4">{{ title }}</span></div>
        <div class="col-md-4">
            <form class="form-inline" method="get">
                <div class="input-group">
                    <input type="text" name="q" class="form-control" placeholder="Quick Search"
                           value="{{ search_text or '' }}" />
                    <div class="input-group-btn">
                        <button type="submit" class="btn btn-default">
                            <i class="glyphicon glyphicon-search"></i>
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>

<div class="panel panel-default capture-list">
    <div class="panel-body" style="padding-bottom:0;">
      <form data-bind="table" method="post" data-paging-numbers="{{ records.paging_numbers }}">
        <table class="table table-condensed table-hover table-striped" style="margin-bottom:0; padding-bottom:0;">
            <thead>
                <tr><th>Enum.ID</th>
                    <th>R.Seqence</th>
                    <th>Customer</th>
                    <th>Address</th>
                    <th>Mobile #</th>
                    <th>Acct. Status</th>
                    <th>Acct. #</th>
                    <th>Tariff</th>
                    <th>Meter</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            % if records:
                % for r in records:
                <tr><td>{{! enum(r.enum_id) }}</td>
                    <td><a href="{{ r._id }}/">{{ r.rseq }}</a></td>
                    <td>{{ shorten(f(r.cust_name)).title() }}</td>
                    <td>{{ shorten("%s %s" % (addy(r.addy_no), addy(r.addy_street))).title() }}
                    <td>{{ f(r.cust_mobile1 or r.cust_mobile2) }}</td>
                    <td>{{ r.acct_status }}</td>
                    <td>{{ f(r.acct_no) }}</td>
                    <td>{{ f(r.tariff) }}</td>
                    <td>{{ f(r.meter_type) }}</td>
                    <td><i class="glyphicon glyphicon-none"></i></td>
                </tr>
                % end
            % else:
                <tr><td colspan="10">No data available</td></tr>
            % end
            </tbody>
            <tfoot>
                <tr><td colspan="10">
                    % include('table-footer.tpl', p=records)
                    </td></tr>
            </tfoot>
        </table>
      </form>
    </div>
</div>
% include('filter-panel.tpl', q=filter_params)
% def scripts():
    <script type="text/javascript">
        App.filterCapture();
        $('.input-group.date').datepicker({
                format: "yyyy-mm-dd", clearBtn: true,
                autoclose: true, toggleActive: true,
                todayHighlight: true,           
            });
    </script>
% end
% rebase('layout.tpl', title=title, year=year, extra_scripts=scripts)