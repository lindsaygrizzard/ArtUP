   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Description: requests toolbelt
        =================
        
        This is just a collection of utilities for `python-requests`_, but don't 
        really belong in ``requests`` proper. The minimum tested requests version is 
        ``2.1.0``. In reality, the toolbelt should work with ``2.0.1`` as well, but 
        some idiosyncracies prevent effective or sane testing on that version.
        
        
        multipart/form-data Encoder
        ---------------------------
        
        The main attraction is a streaming multipart form-data object, ``MultipartEncoder``.
        Its API looks like this:
        
        .. code-block:: python
        
            from requests_toolbelt import MultipartEncoder
            import requests
        
            m = MultipartEncoder(
                fields={'field0': 'value', 'field1': 'value',
                        'field2': ('filename', open('file.py', 'rb'), 'text/plain')}
                )
        
            r = requests.post('http://httpbin.org/post', data=m,
                              headers={'Content-Type': m.content_type})
        
        
        You can also use ``multipart/form-data`` encoding for requests that don't
        require files:
        
        .. code-block:: python
        
            from requests_toolbelt import MultipartEncoder
            import requests
        
            m = MultipartEncoder(fields={'field0': 'value', 'field1': 'value'})
        
            r = requests.post('http://httpbin.org/post', data=m,
                              headers={'Content-Type': m.content_type})
        
        
        Or, you can just create the string and examine the data:
        
        .. code-block:: python
        
            # Assuming `m` is one of the above
            m.to_string()  # Always returns unicode
        
        
        User-Agent constructor
        ----------------------
        
        You can easily construct a requests-style ``User-Agent`` string::
        
            from requests_toolbelt import user_agent
        
            headers = {
                'User-Agent': user_agent('my_package', '0.0.1')
                }
        
            r = requests.get('https://api.github.com/users', headers=headers)
        
        
        SSLAdapter
        ----------
        
        The ``SSLAdapter`` was originally published on `Cory Benfield's blog`_. 
        This adapter allows the user to choose one of the SSL protocols made available 
        in Python's ``ssl`` module for outgoing HTTPS connections:
        
        .. code-block:: python
        
            from requests_toolbelt import SSLAdapter
            import requests
            import ssl
        
            s = requests.Session()
            s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))
        
        
        Known Issues
        ------------
        
        On Python 3.3.0 and 3.3.1, the standard library's ``http`` module will fail
        when passing an instance of the ``MultipartEncoder``. This is fixed in later
        minor releases of Python 3.3. Please consider upgrading to a later minor
        version or Python 3.4. *There is absolutely nothing this library can do to
        work around that bug.*
        
        .. _Cory Benfield's blog: https://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/
        .. _python-requests: https://github.com/kennethreitz/requests
        
        
        History
        =======
        
        0.4.0 -- 2015-04-03
        -------------------
        
        For more information about this release, please see `milestone 0.4.0 
        <https://github.com/sigmavirus24/requests-toolbelt/issues/46>`_ on the 
        project's page.
        
        New Features
        ~~~~~~~~~~~~
        
        - A naive implemenation of a thread pool is now included in the toolbelt. See 
          the docs in ``docs/threading.rst`` or on `Read The Docs 
          <https://toolbelt.readthedocs.org>`_.
        
        - The ``StreamingIterator`` now accepts files (such as ``sys.stdin``) without 
          a specific length and will properly stream them.
        
        - The ``MultipartEncoder`` now accepts exactly the same format of fields as 
          requests' ``files`` parameter does. In other words, you can now also pass in 
          extra headers to add to a part in the body. You can also now specify a 
          custom ``Content-Type`` for a part.
        
        - An implementation of HTTP Digest Authentication for Proxies is now included.
        
        - A transport adapter that allows a user to specify a specific Certificate 
          Fingerprint is now included in the toolbelt.
        
        - A transport adapter that simplifies how users specify socket options is now 
          included.
        
        - A transport adapter that simplifies how users can specify TCP Keep-Alive 
          options is now included in the toolbelt.
        
        - Deprecated functions from ``requests.utils`` are now included and 
          maintained.
        
        - An authentication tool that allows users to specify how to authenticate to 
          several different domains at once is now included.
        
        - A function to save streamed responses to disk by analyzing the 
          ``Content-Disposition`` header is now included in the toolbelt.
        
        Fixed Bugs
        ~~~~~~~~~~
        
        - The ``MultipartEncoder`` will now allow users to upload files larger than 
          4GB on 32-bit systems.
        
        - The ``MultipartEncoder`` will now accept empty unicode strings for form 
          values.
        
        0.3.1 -- 2014-06-23
        -------------------
        
        - Fix the fact that 0.3.0 bundle did not include the ``StreamingIterator``
        
        0.3.0 -- 2014-05-21
        -------------------
        
        Bug Fixes
        ~~~~~~~~~
        
        - Complete rewrite of ``MultipartEncoder`` fixes bug where bytes were lost in
          uploads
        
        New Features
        ~~~~~~~~~~~~
        
        - ``MultipartDecoder`` to accept ``multipart/form-data`` response bodies and
          parse them into an easy to use object.
        
        - ``SourceAddressAdapter`` to allow users to choose a local address to bind
          connections to.
        
        - ``GuessAuth`` which accepts a username and password and uses the
          ``WWW-Authenticate`` header to determine how to authenticate against a
          server.
        
        - ``MultipartEncoderMonitor`` wraps an instance of the ``MultipartEncoder``
          and keeps track of how many bytes were read and will call the provided
          callback.
        
        - ``StreamingIterator`` will wrap an iterator and stream the upload instead of
          chunk it, provided you also provide the length of the content you wish to
          upload.
        
        0.2.0 -- 2014-02-24
        -------------------
        
        - Add ability to tell ``MultipartEncoder`` which encoding to use. By default
          it uses 'utf-8'.
        
        - Fix #10 - allow users to install with pip
        
        - Fix #9 - Fix ``MultipartEncoder#to_string`` so that it properly handles file
          objects as fields
        
        0.1.2 -- 2014-01-19
        -------------------
        
        - At some point during development we broke how we handle normal file objects.
          Thanks to @konomae this is now fixed.
        
        0.1.1 -- 2014-01-19
        -------------------
        
        - Handle ``io.BytesIO``-like objects better
        
        0.1.0 -- 2014-01-18
        -------------------
        
        - Add initial implementation of the streaming ``MultipartEncoder``
        
        - Add initial implementation of the ``user_agent`` function
        
        - Add the ``SSLAdapter``
        
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: License :: OSI Approved
Classifier: Intended Audience :: Developers
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.2
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: Implementation :: CPython
