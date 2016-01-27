<div class="panel panel-default">
    <div class="panel-heading">
        {{ title }}
    
        <div class="pull-right" style="margin-top:-5px">
            <form method="post" action="sync">
                <button type="submit" name="sync" class="btn btn-primary">Sync</button>
                <input type="hidden" name="project_id" value="{{ project.id }}" />
                <input type="hidden" name="project_xforms" value="" />
            </form>
        </div>    
    </div>
    <div class="panel-body">
        % fmt = '<label class="item-title"><input type="checkbox" value="%s" />&nbsp; %s</label>'
        % include('summary-table.tpl', records=records, header="XForms", 
        %         get_url=lambda r:'#', get_title=lambda r: (fmt % (r.id, r.title[:9])))
    </div>
</div>
% def script():
<script type="text/javascript">
    (function($){
        $(function(){
            $('[name=sync]').on('click', function(){
                var $selected = $('.item-title>input:checked')
                  , form_ids = [];
                if ($selected.length <= 0) {
                    alert('At least one XForm needs to be selected.')
                    return false;
                }
                $selected.each(function() { form_ids.push(this.value); });
                $('[name=project_xforms]').val(form_ids.join(','));
                return true;
            });
        });
    })(jQuery);
</script>
% end
% rebase('layout-md-sm.tpl', title=title, year=year, extra_scripts=script)