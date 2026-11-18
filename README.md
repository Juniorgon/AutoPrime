# AutoPrime — Sistema de Gestão de Concessionária

Projeto acadêmico individual de Desenvolvimento Web (3º ano TII), construído com Flask e PostgreSQL em arquitetura MVC.

## Funcionalidades
- CRUD de Marcas, Carros e Opcionais.
- Relacionamento 1:N: uma Marca possui vários Carros.
- Relacionamento N:N: Carros podem possuir vários Opcionais e cada Opcional pode estar em vários Carros.
- Upload opcional de foto JPG/PNG armazenada em `LargeBinary` no PostgreSQL.
- Miniatura da foto na listagem; edição sem novo upload preserva a foto anterior.
- Relatório PDF dos veículos de uma marca com ReportLab, data e total.
- Interface responsiva com painel e mensagens flash.

## Requisitos
Python 3.10+ e PostgreSQL. O banco deve ser criado previamente pelo usuário `postgres`.

## Instalação
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

Copie `.env.exemplo` para `.env`, altere a senha e crie o banco `concessionaria` no PostgreSQL:
```sql
CREATE DATABASE concessionaria;
```

Depois execute:
```bash
flask --app run.py db upgrade
python run.py
```

A aplicação estará em http://127.0.0.1:5000.

> A pasta `migrations/` já contém a revisão inicial versionada. Para alterações futuras, use `flask --app run.py db migrate -m "descrição"` e revise o arquivo gerado antes de versioná-lo.

## Estrutura
```text
app/
  controllers/   # um controller por entidade + painel/relatórios
  models/        # modelos e tabela associativa
  templates/     # templates separados por entidade
  static/css/
  forms.py
config.py
run.py
migrations/
requirements.txt
.env.exemplo
```

## Observações
- Não inclua `.env`, senhas, ambiente virtual ou `__pycache__` no envio.
- O campo de foto aceita JPG/JPEG/PNG e o limite geral de upload é 5 MB.
- O banco não é criado automaticamente pela aplicação: crie-o no PostgreSQL antes de executar as migrations.
