from features.associations import models as associations_models, predicates as associations_rules
import rules


@rules.predicate
def can_view(user, association):
    return associations_models.Association.objects.can_view(user, container='content') \
            .filter(pk=association.pk).exists()


rules.add_perm(
        'content.list',
        rules.always_allow)

rules.add_perm(
        'content.view',
        can_view)

rules.add_perm(
        'content.comment',
        rules.is_authenticated & can_view)

rules.add_perm(
        'content.create',
        rules.is_authenticated)

rules.add_perm(
        'content.group_create',
        rules.is_authenticated & associations_rules.is_member)

rules.add_perm(
        'content.change',
        rules.is_authenticated & associations_rules.is_member)