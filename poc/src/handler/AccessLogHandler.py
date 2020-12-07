from ..Route import Decorator
class AccessLogHandler(Decorator):
    '''
    * <h1>Access Log Handler</h1>
    * <p>
    * Log incoming requested using the
    * <a href="https://en.wikipedia.org/wiki/Common_Log_Format">NCSA format</a> (a.k.a common log
    * format).
    * </p>
    *
    * If you run behind a reverse proxy that has been configured to send the X-Forwarded-* header,
    * please consider to set {@link Router#setTrustProxy(boolean)} option.
    *
    * <h2>usage</h2>
    *
    * <pre>{@code
    * {
    *   decorator(new AccessLogHandler());
    *
    *   ...
    * }
    * }</pre>
    *
    * <p>
    * Output looks like:
    * </p>
    *
    * <pre>
    * 127.0.0.1 - - [04/Oct/2016:17:51:42 +0000] "GET / HTTP/1.1" 200 2
    * </pre>
    *
    * <p>
    * You probably want to configure the <code>AccessLogHandler</code> logger to save output into a new file:
    * </p>
    *
    * <pre>
    * &lt;appender name="ACCESS" class="ch.qos.logback.core.rolling.RollingFileAppender"&gt;
    *   &lt;file&gt;access.log&lt;/file&gt;
    *   &lt;rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy"&gt;
    *     &lt;fileNamePattern&gt;access.%d{yyyy-MM-dd}.log&lt;/fileNamePattern&gt;
    *   &lt;/rollingPolicy&gt;
    *
    *   &lt;encoder&gt;
    *     &lt;pattern&gt;%msg%n&lt;/pattern&gt;
    *   &lt;/encoder&gt;
    * &lt;/appender&gt;
    *
    * &lt;logger name="io.jooby.AccessLogHandler" additivity="false"&gt;
    *   &lt;appender-ref ref="ACCESS" /&gt;
    * &lt;/logger&gt;
    * </pre>
    *
    * <p>
    * By defaults it log the available user context: {@link Context#getUser()}. To override this:
    * </p>
    *
    * <pre>{@code
    * {
    *
    *   decorator("*", new AccessLogHandler(ctx -> {
    *     // retrieve user ID from context.
    *   }));
    * }
    * }</pre>
    *
    * <h2>custom log function</h2>
    * <p>
    * By default it uses the underlying logging system: <a href="http://logback.qos.ch">logback</a>.
    * That's why we previously show how to configure the <code>io.jooby.AccessLogHandler</code> in
    * <code>logback.xml</code>.
    * </p>
    *
    * <p>
    * If you want to log somewhere else and/or use a different method then:
    * </p>
    *
    * <pre>{@code
    * {
    *   use("*", new AccessLogHandler()
    *     .log(line -> {
    *       System.out.println(line);
    *     }));
    * }
    * }</pre>
    *
    * <p>
    * This is just an example but of course you can log the <code>NCSA</code> line to database, jms
    * queue, etc...
    * </p>
    *
    * <h2>latency</h2>
    *
    * <pre>{@code
    * {
    *   use("*", new RequestLogger()
    *       .latency());
    * }
    * }</pre>
    *
    * <p>
    * It add a new entry at the last of the <code>NCSA</code> output that represents the number of
    * <code>ms</code> it took to process the incoming release.
    *
    * <h2>request and response headers</h2>
    * <p>
    * You can add extra headers using the {@link AccessLogHandler#requestHeader(String...)} and
    * {@link AccessLogHandler#responseHeader(String...)}
    * </p>
    *
    * <h2>dateFormatter</h2>
    *
    * <pre>{@code
    * {
    *   use("*", new RequestLogger()
    *       .dateFormatter(ts -> ...));
    *
    *   // OR
    *   use("*", new RequestLogger()
    *       .dateFormatter(DateTimeFormatter...));
    * }
    * }</pre>
    *
    * <p>
    * You can provide a function or an instance of {@link DateTimeFormatter}.
    * </p>
    *
    * <p>
    * The default formatter use the default server time zone, provided by
    * {@link ZoneId#systemDefault()}. It's possible to just override the time zone (not the entirely
    * formatter) too:
    * </p>
    *
    * <pre>{@code
    * {
    *   use("*", new RequestLogger()
    *      .dateFormatter(ZoneId.of("UTC"));
    * }
    * }</pre>
    *
    * @author edgar
    * @since 2.5.2
    '''
    def __init__(self, userId):
        self.USER_AGENT = "User-Agent"
        self.REFERER = "Referer"
        #self.FORMATTER = 
        self.DASH = "-"
        self.SP = ' '
        self.BL = '['
        self.BR = ']'
        self.Q = '\"'
        #self.USER_OR_DASH = lambda
        self.MESSAGE_SIZE = 256
        self.userId = userId if len(userId) else None