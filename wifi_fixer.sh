#!/bin/bash
# The latest version of this package is available at:
# <http://github.com/jantman/pi2graphite>
#
##################################################################################
# Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
#
#    This file is part of pi2graphite, also known as pi2graphite.
#
#    pi2graphite is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pi2graphite is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with pi2graphite.  If not, see <http://www.gnu.org/licenses/>.
#
# The Copyright and Authors attributions contained herein may not be removed or
# otherwise altered, except to add the Author attribution of a contributor to
# this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
###################################################################################
# While not legally required, I sincerely request that anyone who finds
# bugs please submit them at <https://github.com/jantman/pi2graphite> or
# to me via email, and that you send any contributions or improvements
# either as a pull request on GitHub, or to me via email.
##################################################################################
#
# AUTHORS:
# Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################

DEVNAME=$(iw dev | grep 'Interface' | awk '{print $2}' | head -1)

# Exit now if we're associated
if ! iwconfig $DEVNAME | head -1 | grep unassociated >&/dev/null; then
    # we're not unassociated, which means we're associated
    # remove the lockfile and exit
    rm -f /root/.wifi_fixer_last_unassoc
    exit 0
fi

if [[ ! -e /root/.wifi_fixer_last_unassoc ]]; then
    # lockfile doesn't exist, this is the first unassoc
    # touch it and wait for the next run
    touch /root/.wifi_fixer_last_unassoc
    exit 0
fi

# ok, if we got here, we've been unassoc for at least one cron interval
echo "pi2graphite.$(hostname).${DEVNAME}.wifi-fixer 1 $(date +%s)" > /var/lib/pi2graphite/$(date +%s)-wififixer
logger -t wifi_fixer.sh "Killing wpa_supplicant and forcing up $DEVNAME"
killall /sbin/wpa_supplicant
ifup --force $DEVNAME
