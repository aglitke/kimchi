/*
 * Project Kimchi
 *
 * Copyright IBM, Corp. 2013
 *
 * Authors:
 *  Adam Litke <agl@linux.vnet.ibm.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
kimchi.login_main = function() {
	var doLogin = function(event) {
        var settings = {'userid': $("#userid").val(),
                        'password': $("#password").val()};
        kimchi.login(settings, function() {
            /*
             * Now with the session established, reloading the page
             * should display the real content.
             */
            location.reload(true);
		},function() {
			kimchi.message.error(i18n['login.msg.login.failed']);
		});

		return false;
	};

	$('#form-login').on('submit', doLogin);
	$('#doLogin').on('click', doLogin);
};
