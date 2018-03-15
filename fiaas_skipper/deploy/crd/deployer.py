#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import

import logging

from k8s.client import ClientError

from .types import FiaasApplicationSpec, FiaasApplication
from ..deploy import Deployer, generate_config, default_config_template

LOG = logging.getLogger(__name__)


class CrdDeployer(Deployer):
    def _deploy(self, deployment_config, channel):
        LOG.info("Deploying %s to %s", deployment_config.name, deployment_config.namespace)
        try:
            fdd_app = FiaasApplication(metadata=self._create_metadata(deployment_config),
                                       spec=self._create_application_spec(name=deployment_config.name,
                                                                          namespace=deployment_config.namespace,
                                                                          image=channel.metadata['image']))
            fdd_app.save()
        except ClientError as e:
            if e.response.json()['reason'] != 'AlreadyExists':
                raise

    def _create_application_spec(self, name, namespace, image):
        config = generate_config(default_config_template, namespace, self._ingress_suffix)
        return FiaasApplicationSpec(application=name, image=image, config=config)
