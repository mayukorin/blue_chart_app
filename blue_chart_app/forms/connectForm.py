from django import forms


class ConnectForNotOvercomeLatestConnectsForm(forms.Form):

    is_overcome = forms.BooleanField(required=False)

    def __init__(self, latest_connect, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.latest_connect_cache = latest_connect
        self.cause_tag_cache = latest_connect.cause_tag

        if self.errors:
            print(self.errors)

    def get_latest_connect_cache(self):

        return self.latest_connect_cache

    def get_cause_tag_cache(self):

        return self.cause_tag_cache
