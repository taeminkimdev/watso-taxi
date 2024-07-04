import pymysql.cursors
from dependency_injector import containers, providers
from pymysql import connect
from config.production import mysql

from domain.group.application.group_service import GroupService
from domain.group.persistance.group_repository import MySQLGroupRepository
from domain.taxi_group.persistance.taxi_group_repository import MySQLTaxiGroupRepository
from domain.taxi_group.persistance.taxi_group_query_dao import MySQLTaxiGroupQueryDao
from domain.taxi_group.application.taxi_group_service import TaxiGroupService


class TaxiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.taxi_group.command',
                                                            'app.api.taxi_group.query'])

    mysql_connection = providers.Singleton(
        connect,
        host=mysql.host,
        user=mysql.user,
        password=mysql.password,
        port=mysql.port,
        database=mysql.database
    )

    group_repository = providers.Singleton(MySQLGroupRepository, mysql_connection=mysql_connection)
    taxi_group_repository = providers.Singleton(MySQLTaxiGroupRepository, mysql_connection=mysql_connection)
    taxi_group_query_dao = providers.Singleton(MySQLTaxiGroupQueryDao, mysql_connection=mysql_connection)

    group_service = providers.Singleton(GroupService, group_repository=group_repository)
    taxi_group_service = providers.Singleton(
        TaxiGroupService,
        group_service=group_service,
        group_repository=group_repository,
        taxi_group_repository=taxi_group_repository
    )
