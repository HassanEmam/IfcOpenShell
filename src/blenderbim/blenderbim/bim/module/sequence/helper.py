# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2020, 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.

import bpy
import math
import isodate
import datetime
from dateutil import parser
from ifcopenshell.api.sequence.data import Data


def derive_date(ifc_definition_id, attribute_name, date=None, is_earliest=False, is_latest=False):
    task = Data.tasks[ifc_definition_id]
    if task["TaskTime"]:
        current_date = Data.task_times[task["TaskTime"]][attribute_name]
        if current_date:
            return current_date
    for subtask in task["RelatedObjects"]:
        current_date = derive_date(subtask, attribute_name, date=date, is_earliest=is_earliest, is_latest=is_latest)
        if is_earliest:
            if current_date and (date is None or current_date < date):
                date = current_date
        if is_latest:
            if current_date and (date is None or current_date > date):
                date = current_date
    return date


def derive_duration(ifc_definition_id, attribute_name):
    task = Data.tasks[ifc_definition_id]
    if task["TaskTime"]:
        current_date = Data.task_times[task["TaskTime"]][attribute_name]
        if current_date:
            return current_date
    for subtask in task["RelatedObjects"]:
        current_date = derive_date(subtask, attribute_name, date=date, is_earliest=is_earliest, is_latest=is_latest)
        if is_earliest:
            if current_date and (date is None or current_date < date):
                date = current_date
        if is_latest:
            if current_date and (date is None or current_date > date):
                date = current_date
    return date


def parse_datetime(value):
    try:
        return parser.isoparse(value)
    except:
        try:
            return parser.parse(value, dayfirst=True, fuzzy=True)
        except:
            return None


def parse_duration(value):
    try:
        return isodate.parse_duration(value)
    except:
        return None


def canonicalise_time(time):
    if not time:
        return "-"
    return time.strftime("%d/%m/%y")
