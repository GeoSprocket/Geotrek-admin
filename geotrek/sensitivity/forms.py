from django import forms
from .models import SensitiveArea, SportPractice, Species
from geotrek.common.forms import CommonForm
from django.utils.translation import pgettext, ugettext as _
from mapentity.widgets import MapWidget


class BubbleMapWidget(MapWidget):
    geometry_field_class = 'bubbleGeometryField'


class PolygonMapWidget(MapWidget):
    geometry_field_class = 'polygonGeometryField'


class SensitiveAreaForm(CommonForm):
    geomfields = ['geom']
    edit_structure = True
    species = forms.ModelChoiceField(queryset=Species.objects.filter(category=Species.SPECIES),
                                     label=pgettext(u"Singular", u"Species"))

    class Meta:
        fields = ['species', 'published', 'description', 'contact', 'geom', 'structure']
        model = SensitiveArea
        widgets = {'geom': BubbleMapWidget()}


class RegulatorySensitiveAreaForm(CommonForm):
    geomfields = ['geom']
    name = forms.CharField(max_length=250, label=_(u"Name"))
    pictogram = forms.FileField(label=_(u"Pictogram"), required=False)
    period01 = forms.BooleanField(label=_(u"January"), required=False)
    period02 = forms.BooleanField(label=_(u"February"), required=False)
    period03 = forms.BooleanField(label=_(u"March"), required=False)
    period04 = forms.BooleanField(label=_(u"April"), required=False)
    period05 = forms.BooleanField(label=_(u"May"), required=False)
    period06 = forms.BooleanField(label=_(u"June"), required=False)
    period07 = forms.BooleanField(label=_(u"July"), required=False)
    period08 = forms.BooleanField(label=_(u"August"), required=False)
    period09 = forms.BooleanField(label=_(u"September"), required=False)
    period10 = forms.BooleanField(label=_(u"October"), required=False)
    period11 = forms.BooleanField(label=_(u"November"), required=False)
    period12 = forms.BooleanField(label=_(u"Decembre"), required=False)
    practices = forms.ModelMultipleChoiceField(label=_(u"Sport practices"), queryset=SportPractice.objects)
    url = forms.URLField(label=_(u"URL"), required=False)

    class Meta:
        fields = ['name', 'published', 'description', 'contact', 'pictogram', 'practices'] + \
                 ['period{:02}'.format(p) for p in range(1, 13)] + ['url', 'geom', 'structure']
        model = SensitiveArea
        widgets = {'geom': PolygonMapWidget()}

    def __init__(self, *args, **kwargs):
        if kwargs['instance']:
            species = kwargs['instance'].species
            kwargs['initial'] = {
                'name': species.name,
                'pictogram': species.pictogram,
                'practices': species.practices.all(),
                'url': species.url,
            }
            for p in range(1, 13):
                name = 'period{:02}'.format(p)
                kwargs['initial'][name] = getattr(species, name)
        super(RegulatorySensitiveAreaForm, self).__init__(*args, **kwargs)
        self.helper.form_action += '?category=2'

    def save(self):
        if not self.instance.pk:
            species = Species()
        else:
            species = self.instance.species
        species.category = Species.REGULATORY
        species.name = self.cleaned_data['name']
        species.pictogram = self.cleaned_data['pictogram']
        species.url = self.cleaned_data['url']
        for p in range(1, 13):
            fieldname = 'period{:02}'.format(p)
            setattr(species, fieldname, self.cleaned_data[fieldname])
        species.save()
        species.practices = self.cleaned_data['practices']
        area = super(RegulatorySensitiveAreaForm, self).save(commit=False)
        area.species = species
        area.save()
        return area
