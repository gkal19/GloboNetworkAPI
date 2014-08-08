# -*- coding:utf-8 -*-
'''
Title: Infrastructure NetworkAPI
Author: masilva / S2IT
Copyright: ( c )  2012 globo.com todos os direitos reservados.
'''

from django.forms.models import model_to_dict
from networkapi.admin_permission import AdminPermission
from networkapi.auth import has_perm
from networkapi.exception import InvalidValueError
from networkapi.grupo.models import GrupoError, UGrupo, UGrupoNotFoundError
from networkapi.usuario.models import Usuario, UsuarioGrupo, UsuarioError, UsuarioNotFoundError, UsuarioGrupoDuplicatedError, UserGroupNotFoundError
from networkapi.infrastructure.xml_utils import dumps_networkapi
from networkapi.log import Log
from networkapi.rest import RestResource, UserNotAuthorizedError
from networkapi.util import is_valid_int_greater_zero_param

class UserGroupAssociateResource(RestResource):

    log = Log('UserGroupAssociateResource')

    def handle_put(self, request, user, *args, **kwargs):
        """Treat PUT requests to associate User and Group.

        URL: usergroup/user/<id_user>/ugroup/<id_group>/associate/
        """
        
        try:
            
            self.log.info("Associate User and Group.")
            
            # User permission
            if not has_perm(user, AdminPermission.USER_ADMINISTRATION, AdminPermission.WRITE_OPERATION):
                self.log.error(u'User does not have permission to perform the operation.')
                raise UserNotAuthorizedError(None)
            
            id_user = kwargs.get('id_user')
            id_group = kwargs.get('id_group')
            
            # Valid ID User
            if not is_valid_int_greater_zero_param(id_user):
                self.log.error(u'The id_user parameter is not a valid value: %s.', id_user)
                raise InvalidValueError(None, 'id_user', id_user)
            
            # Valid ID Group
            if not is_valid_int_greater_zero_param(id_group):
                self.log.error(u'The id_group parameter is not a valid value: %s.', id_group)
                raise InvalidValueError(None, 'id_group', id_group)
            
            # Find User by ID to check if it exist
            usr = Usuario.get_by_pk(id_user)
            
            # Find Group by ID to check if it exist
            group = UGrupo.get_by_pk(id_group)
            
            try:
                
                # Find UserGroup by ID to check if it exist
                user_group = UsuarioGrupo.get_by_user_group(id_user, id_group)
                raise UsuarioGrupoDuplicatedError(None, u'Usuário já está associado ao Grupo.')
            except UserGroupNotFoundError:
                pass
            
            user_group = UsuarioGrupo()
            
            # set variables
            user_group.usuario = usr
            user_group.ugrupo = group
            
            try:
                # save UserGroup
                user_group.save(user)
            except Exception, e:
                self.log.error(u'Failed to save the UserGroup.')
                raise UsuarioError(e, u'Failed to save the UserGroup.')
            
            usr_grp_map = dict()
            usr_grp_map['user_group'] = model_to_dict(usr, exclude=["usuario", "ugrupo"])
            
            return self.response(dumps_networkapi(usr_grp_map))

        except InvalidValueError, e:
            return self.response_error(269, e.param, e.value)
        
        except UserNotAuthorizedError:
            return self.not_authorized()
        
        except UsuarioGrupoDuplicatedError:
            return self.response_error(183, id_user, id_group) 

        except UsuarioNotFoundError:
            return self.response_error(177, id_user)
        
        except UGrupoNotFoundError:
            return self.response_error(180, id_group)
        
        except (GrupoError, UsuarioError):
            return self.response_error(1)