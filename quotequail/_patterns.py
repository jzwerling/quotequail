# -*- coding: utf-8 -*-

import re

REPLY_PATTERNS = [
    u'^On (.*) wrote:$', # apple mail/gmail reply
    u'^Am (.*) schrieb (.*):$', # German
    u'^Le (.*) a écrit :$', # French
    u'El (.*) escribió:$', # Spanish
    u'^(.*) написал\(а\):$',  # Russian
    u'^Den (.*) skrev (.*):$', # Swedish
    u'([0-9]{4}/[0-9]{1,2}/[0-9]{1,2}) (.* <.*@.*>)$', # gmail (?) reply
]

REPLY_DATE_SPLIT_REGEX = re.compile(r'^(.*(:[0-9]{2}( [apAP]\.?[mM]\.?)?)), (.*)?$')

FORWARD_MESSAGES = [
    # apple mail forward
    'Begin forwarded message', 'Anfang der weitergeleiteten E-Mail',
    u'Début du message réexpédié', 'Inicio del mensaje reenviado',

    # gmail/evolution forward
    'Forwarded [mM]essage', 'Mensaje reenviado', 'Vidarebefordrat meddelande',

    # outlook
    'Original [mM]essage', 'Ursprüngliche Nachricht', 'Mensaje [oO]riginal',

    # Thunderbird forward
    u'Message transféré',

    # mail.ru forward (Russian)
    u'Пересылаемое сообщение',

    #chinese, qq mail, hotmail, last is from lotus notes
    u'原始邮件', u'转发邮件信息', u'轉呈者',
    #japanese
    u'元のメール', u'電子メール情報の転送', u'フォワーダ', u'転送者', u'元のメッセージ',
    #korean
    u'원본 메일', u'전자 메일 정보 전달', u'전달자'

]

# We yield this pattern to simulate Outlook forward styles. It is also used for
# some emails forwarded by Yahoo.
FORWARD_LINE = '________________________________'

FORWARD_PATTERNS = [
    '^{}$'.format(FORWARD_LINE),

] + ['^---+ ?%s ?---+$' % p for p in FORWARD_MESSAGES] \
  + ['^%s:$' % p for p in FORWARD_MESSAGES]

FORWARD_STYLES = [
    # Outlook
    'border:none;border-top:solid #B5C4DF 1.0pt;padding:3.0pt 0in 0in 0in',
]

HEADER_RE = re.compile(r'\*?([-\w ]+):\*?(.*)$', re.UNICODE)

HEADER_MAP = {
    'from': 'from',
    'von': 'from',
    'de': 'from',
    u'от кого': 'from',
    u'från': 'from',
    u'发件人': 'from', #cn
    u'从': 'from', #cn
    u'差出人': 'from', #jp
    u'送信者': 'from', #jp
    u'작성자': 'from', #ko
    u'보낸 사람': 'from', #ko


    'to': 'to',
    'an': 'to',
    'para': 'to',
    u'à': 'to',
    u'pour': 'to',
    u'кому': 'to',
    u'till': 'to',
    u'收件人': 'to',  #cn
    u'送至': 'to', #cn
    u'宛先': 'to', #jp
    u'受信者': 'to', #jp
    u'받는 사람': 'to', #ko
    u'수신인': 'to', #ko recipient

    'cc': 'cc',
    'kopie': 'cc',
    'kopia': 'cc',
    u'抄送': 'cc', #cn
    u'副本抄送': 'cc', #cn
    u'참조': 'cc', #ko

    'bcc': 'bcc',
    'cco': 'bcc',
    'blindkopie': 'bcc',
    u'密送': 'bcc', #cn
    u'副本密送': 'bcc', #cn
    u'숨은 참조': 'bcc', #ko

    'reply-to': 'reply-to',
    'antwort an': 'reply-to',
    u'répondre à': 'reply-to',
    'responder a': 'reply-to',

    'date': 'date',
    'sent': 'date',
    'received': 'date',
    'datum': 'date',
    'gesendet': 'date',
    'enviado el': 'date',
    'enviados': 'date',
    'fecha': 'date',
    u'дата': 'date',
    u'发送时间': 'date', #cn
    u'发送日期': 'date', #cn
    u'逸信日時': 'date', #jp
    u'送信日時': 'date', #jp
    u'納期': 'date', #jp
    u'日付': 'date', #jp
    u'転送日': 'date', #jp
    u'날짜': 'date', #ko
    u'날짜/시간': 'date', #ko - datetime

    'subject': 'subject',
    'betreff': 'subject',
    'asunto': 'subject',
    'objet': 'subject',
    'sujet': 'subject',
    u'тема': 'subject',
    u'ämne': 'subject',
    u'主题': 'subject', #cn
    u'主旨': 'subject', #cn
    u'件名': 'subject', #jp
    u'주제': 'subject', #ko
    u'제목': 'subject', #ko
}

COMPILED_PATTERN_MAP = {
    'reply': [re.compile(regex) for regex in REPLY_PATTERNS],
    'forward': [re.compile(regex) for regex in FORWARD_PATTERNS],
}

COMPILED_PATTERNS = sum(COMPILED_PATTERN_MAP.values(), [])

MULTIPLE_WHITESPACE_RE = re.compile('\s+')

# Amount to lines to join to check for potential wrapped patterns in plain text
# messages.
MAX_WRAP_LINES = 2

# minimum number of headers that we recognize
MIN_HEADER_LINES = 2

# minimum number of lines to recognize a quoted block
MIN_QUOTED_LINES = 3

# Characters at the end of line where we join lines without adding a space.
# For example, "John <\njohn@example>" becomes "John <john@example>", but
# "John\nDoe" becomes "John Doe".
STRIP_SPACE_CHARS = '<([{"\''
