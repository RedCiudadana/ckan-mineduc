import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckan import model


def get_tags():
    tags = toolkit.get_action('tag_list')(data_dict={
        'all_fields': True,
        'limit': 3,
        'offset': 0,
    })
    return tags


def get_groups():
    groups = toolkit.get_action('group_list')(data_dict={'all_fields': True})
    return groups


def get_latest_packages():
    resources = toolkit.get_action('current_package_list_with_resources')(data_dict={
        'limit': 3,
        'offset': 0,
    })
    return resources


def get_visualizations():
    # values = model.Session.query(model.ResourceView).filter_by(view_type='visualize').all()
    values = model.Session.query(model.ResourceView) \
        .filter(model.ResourceView.view_type.in_(['image_view'])) \
        .all()
    response = list(map(lambda x: x.as_dict(), values))
    response.reverse()
    visualizations = []
    for i in response:
        try:
            resource = toolkit.get_action('resource_show')(
                data_dict={'id': i['resource_id']})
            # clone i and add resource
            visualizations.append(i)
            visualizations[-1]['resource'] = resource
        except:
            pass
    return visualizations[0:5]

def get_category_total():
    return model.Session.query(model.Group) \
        .count()

def get_resource_total():
    return model.Session.query(model.Resource) \
        .count()

class MineducPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'mineduc')
        toolkit.add_resource('assets', 'mineduc')

    # ITemplateHelpers

    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'demo_tags': get_tags,
            'demo_groups': get_groups,
            'demo_latest_packages': get_latest_packages,
            'demo_visualizations': get_visualizations,
            'demo_category_total': get_category_total,
            'demo_resource_total': get_resource_total,
        }
