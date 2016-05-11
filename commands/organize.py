class OrganizeCommand(object):

    def __init__(self, config):
        super(OrganizeCommand, self).__init__()
        import json
        with open(config_path, 'r') as f:
            self._config = json.loads(f.read())
        self._rules = self._load_rules()

    def _load_rules(self, config_path):
            rules = sorted(self._config.rules, lambda r: r.start_date)
            prev_rule = None
            for rule in rules:
                if prev_rule and rule.start_date < prev_rule.end_date:
                    raise ValueError("Rule dates may not overlap")
        return rules

    def process_file(self, input_path, output_dir):
        fmt_klass = self._get_metadata_handler(input_path)
        with fmt_klass(input_path) as file_fmt:
            creation_dt = file_fmt.get_date()
        rule = self._get_rule(creation_date)
        if rule:
            org_format = rule.format
        else:
            org_format = self.config.format
        metadata = {}
        org_dir = org_format % metadata

        _, filename = os.path.split(input_path)
        output_path = os.path.join(output_dir, org_dir, output_filename)

        import shutil
        shutil.copy2(input_path, output_path)
        print '%s -> %s' % (input_path, output_path)

    def _get_rule(self, file_date):
        for rule in self.rules:
            if file_date > rule.start_date and file_date < rule.end_date:
                return rule
        return None
