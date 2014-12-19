/** 
 * Copyright (c) 2014, Patrick Uiterwijk <puiterwijk@redhat.com>
 * All rights reserved.
 *
 * This file is part of JSOpenID.
 *
 * JSOpenID is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * JSOpenID is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with JSOpenID.  If not, see <http://www.gnu.org/licenses/>.
 */

function respondToLogin(targetOrigin, success, data)
{
    // From an iframe, window.parent == parent window
    //  So if we don't have a window.parent, we're certainly not an iframe
    if(window.parent != null)
    {
        // If we don't have this element in the parent window, this is not an auth iframe
        if(window.parent.document.getElementById('jsopenid_ifrm') != null)
        {
            window.parent.postMessage({"success": success,
                                       "data": data},
                                       targetOrigin);
        }
    }
}

function tryBackgroundLogin(login_url, callback_success, callback_failed)
{
    if(window.parent != null)
    {
        // Check if we are called recursively (from within a login attempt)
        if(window.parent.document.getElementById('jsopenid_ifrm') != null)
        {
            return;
        }
    }

    // Create the iframe we are going to use
    ifrm = document.createElement('iframe');
    ifrm.id = 'jsopenid_ifrm';
    ifrm.src = login_url;
    ifrm.style.width = 0;
    ifrm.style.height = 0;
    ifrm.style.visibility = "hidden";

    // Set up for pingbacks
    window.addEventListener('message', function(event)
    {
        // We don't check don't check event.origin, as it wouldn't add anything worthwhile
        //  This would prevent a rogue website from saying "The user is now logged in", but we should *never* trust this anyway
        //  This whole library is only for user convenience
        if(event.source != ifrm.contentWindow)
        {
            // Ignoring response from someone unexpected
            return;
        }
        document.body.removeChild(ifrm);
        if(event.data["success"])
        {
            callback_success(event.data["data"]);
        }
        else
        {
            if(callback_failed != null)
            {
                callback_failed(event.data["data"]);
            }
        }
    }, false);

    // HIT IT!
    document.body.appendChild(ifrm);
}
