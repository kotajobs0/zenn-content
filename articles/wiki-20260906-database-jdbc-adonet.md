---
title: "【Wiki】データベース接続・JDBC/ADO.NET (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: true
---

## はじめに

このWikiは、チームの若手エンジニアがデータベース接続の基本を学び、即座に安全で効率的なコードを書けるようになるためのリファレンスです。今回は、JavaにおけるJDBC（Java Database Connectivity）とC#におけるADO.NETに焦点を当てます。

データベースはあらゆるアプリケーションの基盤であり、その接続方法はソフトウェア開発の根幹をなします。正しく安全に接続・操作することは、アプリケーションの安定性、セキュリティ、パフォーマンスに直結します。

ここでは、単なるコードの書き方だけでなく、なぜそのように書くべきなのか、プロフェッショナルとして知っておくべき考慮事項（メモリ効率、スレッドセーフティ、セキュリティなど）までを解説します。このWikiを参考に、安全で堅牢なデータアクセス層を構築する力を身につけてください。

---

## 1. Java (JDBC)

Javaアプリケーションからリレーショナルデータベースに接続・操作するための標準APIがJDBCです。

### 1.1. 基本概念

JDBCは以下の主要なインターフェースを中心に設計されています。

*   **`Driver`**: 特定のデータベースに接続するための具体的な実装を提供します（例: MySQL Driver, PostgreSQL Driver, H2 Driver）。
*   **`Connection`**: データベースへのセッションを表します。トランザクションの開始・コミット・ロールバックも管理します。
*   **`Statement`**: 静的なSQL文を実行するためのインターフェースです。
*   **`PreparedStatement`**: パラメータ化されたSQL文を実行するためのインターフェースです。SQLインジェクション対策として推奨されます。
*   **`ResultSet`**: SELECT文の結果セットを表します。カーソルを移動して行を順に読み取ります。

### 1.2. 即実行可能なコード例 (Ready-to-Run)

ここでは、軽量なインメモリデータベースであるH2 Databaseを使用します。プロジェクトのセットアップから実行までを説明します。

#### 1.2.1. プロジェクトの準備 (Maven)

まず、Mavenプロジェクトを作成し、`pom.xml` にH2 Databaseの依存関係を追加します。

1.  **Mavenプロジェクトの作成**:
    ```bash
    mvn archetype:generate -DgroupId=com.example -DartifactId=jdbc-sample -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
    cd jdbc-sample
    ```
2.  **`pom.xml` の編集**:
    `jdbc-sample/pom.xml` を開き、`<dependencies>` セクションに以下のH2 Databaseの依存関係を追加します。

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>com.example</groupId>
        <artifactId>jdbc-sample</artifactId>
        <version>1.0-SNAPSHOT</version>

        <properties>
            <maven.compiler.source>11</maven.compiler.source>
            <maven.compiler.target>11</maven.compiler.target>
        </properties>

        <dependencies>
            <!-- H2 Database -->
            <dependency>
                <groupId>com.h2database</groupId>
                <artifactId>h2</artifactId>
                <version>2.2.224</version> <!-- 最新の安定版を確認してください -->
            </dependency>
        </dependencies>
    </project>
    ```

#### 1.2.2. Javaコード (DatabaseConnectionExample.java)

`jdbc-sample/src/main/java/com/example/App.java` を削除し、`jdbc-sample/src/main/java/com/example/DatabaseConnectionExample.java` を作成して以下のコードを記述します。

このコードは、H2インメモリデータベースに接続し、テーブルを作成、データを挿入、そしてデータを読み取る一連の操作を実行します。`try-with-resources` 文を使い、リソース（Connection, Statement, ResultSet）の確実な解放を行っています。

```java
package com.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseConnectionExample {

    // H2 Databaseの接続情報
    // JDBC URL: jdbc:h2:mem:testdb はインメモリデータベース
    // jdbc:h2:~/testdb はファイルベースデータベース (ホームディレクトリにtestdb.mv.dbが作成される)
    private static final String JDBC_URL = "jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1"; // DB_CLOSE_DELAY=-1で接続が閉じてもDBを維持
    private static final String USERNAME = "sa";
    private static final String PASSWORD = "";

    public static void main(String[] args) {
        // try-with-resources文を使用して、Connection, PreparedStatement, ResultSetを自動的に閉じます
        try (Connection connection = DriverManager.getConnection(JDBC_URL, USERNAME, PASSWORD)) {
            System.out.println("データベースに接続しました！");

            // 1. テーブルの作成
            createTable(connection);

            // 2. データの挿入
            insertData(connection, "Alice", "alice@example.com");
            insertData(connection, "Bob", "bob@example.com");

            // 3. データの更新
            updateData(connection, "Alice Smith", "alice@example.com");

            // 4. データの選択（全件取得）
            selectData(connection);

            // 5. データの削除
            deleteData(connection, "Bob");

            // 6. データの選択（削除後確認）
            System.out.println("\n--- データを削除後 ---");
            selectData(connection);

        } catch (SQLException e) {
            System.err.println("データベース操作中にエラーが発生しました: " + e.getMessage());
            e.printStackTrace();
        } finally {
            System.out.println("データベース接続を閉じました。");
        }
    }

    /**
     * テーブルを作成します。
     * @param connection データベース接続
     * @throws SQLException SQLエラーが発生した場合
     */
    private static void createTable(Connection connection) throws SQLException {
        String createSql = "CREATE TABLE IF NOT EXISTS users (" +
                           "id INT AUTO_INCREMENT PRIMARY KEY," +
                           "name VARCHAR(255) NOT NULL," +
                           "email VARCHAR(255) UNIQUE NOT NULL" +
                           ")";
        try (Statement statement = connection.createStatement()) {
            statement.execute(createSql);
            System.out.println("テーブル 'users' を作成または確認しました。");
        }
    }

    /**
     * データを挿入します（PreparedStatementを使用）。
     * @param connection データベース接続
     * @param name ユーザー名
     * @param email メールアドレス
     * @throws SQLException SQLエラーが発生した場合
     */
    private static void insertData(Connection connection, String name, String email) throws SQLException {
        String insertSql = "INSERT INTO users (name, email) VALUES (?, ?)";
        try (PreparedStatement pstmt = connection.prepareStatement(insertSql)) {
            pstmt.setString(1, name);
            pstmt.setString(2, email);
            int rowsAffected = pstmt.executeUpdate();
            System.out.println(rowsAffected + "件のデータを挿入しました: Name=" + name);
        }
    }

    /**
     * データを更新します（PreparedStatementを使用）。
     * @param connection データベース接続
     * @param newName 新しいユーザー名
     * @param email 更新対象のメールアドレス
     * @throws SQLException SQLエラーが発生した場合
     */
    private static void updateData(Connection connection, String newName, String email) throws SQLException {
        String updateSql = "UPDATE users SET name = ? WHERE email = ?";
        try (PreparedStatement pstmt = connection.prepareStatement(updateSql)) {
            pstmt.setString(1, newName);
            pstmt.setString(2, email);
            int rowsAffected = pstmt.executeUpdate();
            System.out.println(rowsAffected + "件のデータを更新しました: New Name=" + newName);
        }
    }

    /**
     * データを検索して表示します（PreparedStatementを使用）。
     * @param connection データベース接続
     * @throws SQLException SQLエラーが発生した場合
     */
    private static void selectData(Connection connection) throws SQLException {
        String selectSql = "SELECT id, name, email FROM users";
        try (PreparedStatement pstmt = connection.prepareStatement(selectSql);
             ResultSet rs = pstmt.executeQuery()) { // executeQueryはSELECT文に使用
            System.out.println("--- users テーブルのデータ ---");
            while (rs.next()) { // 次の行がある限りループ
                int id = rs.getInt("id");
                String name = rs.getString("name");
                String email = rs.getString("email");
                System.out.println("ID: " + id + ", Name: " + name + ", Email: " + email);
            }
        }
    }

    /**
     * データを削除します（PreparedStatementを使用）。
     * @param connection データベース接続
     * @param name 削除対象のユーザー名
     * @throws SQLException SQLエラーが発生した場合
     */
    private static void deleteData(Connection connection, String name) throws SQLException {
        String deleteSql = "DELETE FROM users WHERE name = ?";
        try (PreparedStatement pstmt = connection.prepareStatement(deleteSql)) {
            pstmt.setString(1, name);
            int rowsAffected = pstmt.executeUpdate();
            System.out.println(rowsAffected + "件のデータを削除しました: Name=" + name);
        }
    }
}
```

#### 1.2.3. 実行方法

1.  **コンパイル**:
    ```bash
    mvn compile
    ```
2.  **実行**:
    ```bash
    mvn exec:java -Dexec.mainClass="com.example.DatabaseConnectionExample"
    ```
    または、JARファイルをビルドして実行:
    ```bash
    mvn package
    java -cp target/jdbc-sample-1.0-SNAPSHOT.jar:~/.m2/repository/com/h2database/h2/2.2.224/h2-2.2.224.jar com.example.DatabaseConnectionExample
    ```
    (CLASSPATHはMavenがダウンロードしたH2 JARファイルのパスに合わせる必要があります)

#### 実行結果例

```
データベースに接続しました！
テーブル 'users' を作成または確認しました。
1件のデータを挿入しました: Name=Alice
1件のデータを挿入しました: Name=Bob
1件のデータを更新しました: New Name=Alice Smith
--- users テーブルのデータ ---
ID: 1, Name: Alice Smith, Email: alice@example.com
ID: 2, Name: Bob, Email: bob@example.com
1件のデータを削除しました: Name=Bob

--- データを削除後 ---
--- users テーブルのデータ ---
ID: 1, Name: Alice Smith, Email: alice@example.com
データベース接続を閉じました。
```

### 1.3. バージョン・アップデート情報

*   **Java 7 (JDBC 4.1) 以降**: `try-with-resources` 文が導入されました。これにより、`Connection`, `Statement`, `ResultSet` といったリソースを`finally`ブロックで明示的に閉じる必要がなくなり、コードが簡潔になり、リソースリークのリスクが大幅に低減されました。**現在は `try-with-resources` の利用が強く推奨されます。**
*   **JDBC 4.0 以降 (Java 6)**: `Class.forName("com.mysql.cj.jdbc.Driver");` のように、JDBCドライバーを明示的にロードする必要がなくなりました。ドライバーがクラスパスにあれば、`DriverManager` が自動的に検出してロードします。
*   **Java 8 以降**: `LocalDateTime` や `LocalDate` といった新しい日時APIをJDBCで扱うための `setObject()`/`getObject()` メソッドが追加され、より自然に日時を扱えるようになりました。

### 1.4. プロフェッショナルな視点

#### 1.4.1. リソース管理とメモリ効率

*   **`try-with-resources` の徹底**: データベース接続、ステートメント、結果セットなどのリソースは、使用後に必ず解放しなければなりません。解放を忘れると、データベース接続の枯渇、メモリリーク、パフォーマンス低下の原因となります。`try-with-resources` を使うことで、`AutoCloseable` インターフェースを実装しているオブジェクトはブロック終了時に自動的に `close()` メソッドが呼ばれ、安全にリソースを解放できます。
*   **接続プール (Connection Pool)**: `Connection` オブジェクトの生成と破棄は非常にコストが高い処理です。本番環境や高負荷なアプリケーションでは、接続プール（例: HikariCP, Apache Commons DBCP, Tomcat JDBC Connection Pool）を使用することが必須です。接続プールは、あらかじめデータベース接続を一定数保持しておき、必要な時に貸し出し、使い終わったらプールに戻すことで、接続のオーバーヘッドを削減し、アプリケーションのパフォーマンスとスケーラビリティを向上させます。

#### 1.4.2. スレッドセーフティ

*   **`Connection` はスレッドセーフではない**: 一般的に、JDBCの `Connection` オブジェクトはスレッドセーフではありません。つまり、複数のスレッドが同時に同じ `Connection` オブジェクトを使用してデータベース操作を行うと、データ競合や不整合が発生する可能性があります。
*   **各スレッドが自身の `Connection` を持つ**: スレッドごとに独立した `Connection` を使用するか、接続プールから `Connection` を借りて使用し、使用後は必ずプールに返却する必要があります。接続プールは、スレッドセーフな形で `Connection` オブジェクトを管理し、各リクエスト（スレッド）に対して排他的な `Connection` を提供します。

#### 1.4.3. セキュリティ (SQLインジェクション対策)

*   **`PreparedStatement` の絶対的な利用**: ユーザー入力や外部からのデータを用いてSQL文を構築する際は、必ず `PreparedStatement` を使用してください。`PreparedStatement` は、SQL文とパラメータを分離して扱うため、パラメータがSQLの一部として解釈されることを防ぎ、SQLインジェクション攻撃を根本的に防ぎます。
*   **`Statement` の危険性**: `Statement` を使用し、文字列結合でSQL文を構築することは極めて危険です。

    ```java
    // 悪い例（SQLインジェクションの脆弱性あり）
    String username = getUserInput(); // 例: "admin' OR '1'='1"
    String sql = "SELECT * FROM users WHERE username = '" + username + "'";
    // statement.executeQuery(sql); // 実行すると危険！
    ```

#### 1.4.4. パフォーマンス

*   **`PreparedStatement` の再利用**: `PreparedStatement` はSQL文を事前にコンパイル（プリコンパイル）しておくため、同じSQL文を繰り返し実行する場合にパフォーマンスが向上します。特にループ内で大量のINSERT/UPDATEを行う場合に効果的です。
*   **バッチ処理**: 大量のデータを一度に挿入・更新する場合、`PreparedStatement` のバッチ処理機能 (`addBatch()`, `executeBatch()`) を利用することで、ネットワークI/Oの回数を減らし、大幅なパフォーマンス向上を実現できます。
*   **適切なデータ取得**: `SELECT *` ではなく、必要なカラムのみを指定して取得することで、データベースサーバーとアプリケーション間のネットワークトラフィックを削減し、メモリ使用量も抑えることができます。

---

## 2. C# (ADO.NET)

C#/.NETアプリケーションからリレーショナルデータベースに接続・操作するためのAPIセットがADO.NETです。

### 2.1. 基本概念

ADO.NETは、プロバイダモデルに基づいて設計されており、特定のデータベースに依存しない共通のインターフェースと、特定のデータベース用の具体的なプロバイダ（SQL Server、Oracle、SQLiteなど）から構成されます。

主要なクラス（インターフェース）は以下の通りです。

*   **`DbConnection` (または `SqlConnection`, `SqliteConnection` など)**: データベースへの接続を表します。
*   **`DbCommand` (または `SqlCommand`, `SqliteCommand` など)**: SQL文またはストアドプロシージャを実行するためのオブジェクトです。
*   **`DbDataReader` (または `SqlDataReader`, `SqliteDataReader` など)**: SELECT文の結果を読み取るための、高速で前方のみに移動可能なストリームです。
*   **`DbParameter` (または `SqlParameter`, `SqliteParameter` など)**: パラメータ化クエリで使用するパラメータを表します。
*   **`DbDataAdapter`**: `DataSet` や `DataTable` といったオフラインデータセットとデータベース間の橋渡しをします。

### 2.2. 即実行可能なコード例 (Ready-to-Run)

ここでは、軽量なファイルベースデータベースであるSQLiteを使用します。プロジェクトのセットアップから実行までを説明します。

#### 2.2.1. プロジェクトの準備 (.NET Core / .NET 5+)

1.  **新しいコンソールプロジェクトの作成**:
    ```bash
    dotnet new console -n DbConnectionSample
    cd DbConnectionSample
    ```
2.  **NuGetパッケージの追加**:
    SQLiteに接続するための `Microsoft.Data.SQLite` パッケージを追加します。

    ```bash
    dotnet add package Microsoft.Data.SQLite
    ```

#### 2.2.2. C#コード (Program.cs)

`DbConnectionSample/Program.cs` を開き、以下のコードを記述します。

このコードは、SQLiteファイルデータベースに接続し、テーブルを作成、データを挿入、そしてデータを読み取る一連の操作を実行します。`using` ステートメントを使い、リソース（Connection, Command, DataReader）の確実な解放を行っています。

```csharp
using Microsoft.Data.Sqlite;
using System;
using System.Data;
using System.IO;

public class Program
{
    // SQLiteデータベースファイルのパス
    private static readonly string DbFilePath = "sample.db";
    private static readonly string ConnectionString = $"Data Source={DbFilePath}";

    public static void Main(string[] args)
    {
        // 既存のDBファイルを削除（テスト用）
        if (File.Exists(DbFilePath))
        {
            File.Delete(DbFilePath);
            Console.WriteLine($"既存のデータベースファイル '{DbFilePath}' を削除しました。");
        }

        // usingステートメントを使用して、SqliteConnectionを自動的に閉じます
        using (var connection = new SqliteConnection(ConnectionString))
        {
            try
            {
                connection.Open();
                Console.WriteLine("データベースに接続しました！");

                // 1. テーブルの作成
                CreateTable(connection);

                // 2. データの挿入
                InsertData(connection, "Alice", "alice@example.com");
                InsertData(connection, "Bob", "bob@example.com");

                // 3. データの更新
                UpdateData(connection, "Alice Smith", "alice@example.com");

                // 4. データの選択（全件取得）
                SelectData(connection);

                // 5. データの削除
                DeleteData(connection, "Bob");

                // 6. データの選択（削除後確認）
                Console.WriteLine("\n--- データを削除後 ---");
                SelectData(connection);
            }
            catch (SqliteException ex)
            {
                Console.Error.WriteLine($"データベース操作中にエラーが発生しました: {ex.Message}");
                Console.Error.WriteLine(ex.StackTrace);
            }
            finally
            {
                // usingステートメントがあるので明示的なCloseは不要ですが、例として
                if (connection.State == ConnectionState.Open)
                {
                    connection.Close();
                }
                Console.WriteLine("データベース接続を閉じました。");
            }
        }
    }

    /// <summary>
    /// テーブルを作成します。
    /// </summary>
    /// <param name="connection">データベース接続</param>
    private static void CreateTable(SqliteConnection connection)
    {
        string createSql = "CREATE TABLE IF NOT EXISTS users (" +
                           "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                           "name TEXT NOT NULL," +
                           "email TEXT UNIQUE NOT NULL" +
                           ")";
        using (var command = new SqliteCommand(createSql, connection))
        {
            command.ExecuteNonQuery(); // SELECT文以外でデータの変更を伴うSQLを実行
            Console.WriteLine("テーブル 'users' を作成または確認しました。");
        }
    }

    /// <summary>
    /// データを挿入します（パラメーター化クエリを使用）。
    /// </summary>
    /// <param name="connection">データベース接続</param>
    /// <param name="name">ユーザー名</param>
    /// <param name="email">メールアドレス</param>
    private static void InsertData(SqliteConnection connection, string name, string email)
    {
        string insertSql = "INSERT INTO users (name, email) VALUES (@name, @email)";
        using (var command = new SqliteCommand(insertSql, connection))
        {
            command.Parameters.AddWithValue("@name", name);
            command.Parameters.AddWithValue("@email", email);
            int rowsAffected = command.ExecuteNonQuery();
            Console.WriteLine($"{rowsAffected}件のデータを挿入しました: Name={name}");
        }
    }

    /// <summary>
    /// データを更新します（パラメーター化クエリを使用）。
    /// </summary>
    /// <param name="connection">データベース接続</param>
    /// <param name="newName">新しいユーザー名</param>
    /// <param name="email">更新対象のメールアドレス</param>
    private static void UpdateData(SqliteConnection connection, string newName, string email)
    {
        string updateSql = "UPDATE users SET name = @newName WHERE email = @email";
        using (var command = new SqliteCommand(updateSql, connection))
        {
            command.Parameters.AddWithValue("@newName", newName);
            command.Parameters.AddWithValue("@email", email);
            int rowsAffected = command.ExecuteNonQuery();
            Console.WriteLine($"{rowsAffected}件のデータを更新しました: New Name={newName}");
        }
    }

    /// <summary>
    /// データを検索して表示します（パラメーター化クエリを使用）。
    /// </summary>
    /// <param name="connection">データベース接続</param>
    private static void SelectData(SqliteConnection connection)
    {
        string selectSql = "SELECT id, name, email FROM users";
        using (var command = new SqliteCommand(selectSql, connection))
        {
            using (var reader = command.ExecuteReader()) // ExecuteReaderはSELECT文に使用
            {
                Console.WriteLine("--- users テーブルのデータ ---");
                while (reader.Read()) // 次の行がある限りループ
                {
                    int id = reader.GetInt32(reader.GetOrdinal("id"));
                    string name = reader.GetString(reader.GetOrdinal("name"));
                    string email = reader.GetString(reader.GetOrdinal("email"));
                    Console.WriteLine($"ID: {id}, Name: {name}, Email: {email}");
                }
            }
        }
    }

    /// <summary>
    /// データを削除します（パラメーター化クエリを使用）。
    /// </summary>
    /// <param name="connection">データベース接続</param>
    /// <param name="name">削除対象のユーザー名</param>
    private static void DeleteData(SqliteConnection connection, string name)
    {
        string deleteSql = "DELETE FROM users WHERE name = @name";
        using (var command = new SqliteCommand(deleteSql, connection))
        {
            command.Parameters.AddWithValue("@name", name);
            int rowsAffected = command.ExecuteNonQuery();
            Console.WriteLine($"{rowsAffected}件のデータを削除しました: Name={name}");
        }
    }
}
```

#### 2.2.3. 実行方法

1.  **実行**:
    ```bash
    dotnet run
    ```

#### 実行結果例

```
既存のデータベースファイル 'sample.db' を削除しました。
データベースに接続しました！
テーブル 'users' を作成または確認しました。
1件のデータを挿入しました: Name=Alice
1件のデータを挿入しました: Name=Bob
1件のデータを更新しました: New Name=Alice Smith
--- users テーブルのデータ ---
ID: 1, Name: Alice Smith, Email: alice@example.com
ID: 2, Name: Bob, Email: bob@example.com
1件のデータを削除しました: Name=Bob

--- データを削除後 ---
--- users テーブルのデータ ---
ID: 1, Name: Alice Smith, Email: alice@example.com
データベース接続を閉じました。
```

### 2.3. バージョン・アップデート情報

*   **`using` ステートメントの利用**: C#では、`IDisposable` インターフェースを実装しているオブジェクト（データベース接続、コマンド、データリーダーなど）に対して `using` ステートメントを使用することで、ブロックを抜ける際に自動的に `Dispose()` メソッドが呼ばれ、リソースが確実に解放されます。**現在ではこの利用が強く推奨されます。**
*   **C# 8.0 以降の `using` 宣言**: `using (var reader = command.ExecuteReader())` の代わりに `using var reader = command.ExecuteReader();` のように、変数を宣言する際に `using` キーワードを付与できるようになりました。これにより、スコープの終端で自動的に `Dispose` が呼ばれます。
*   **非同期処理 (`async`/`await`)**: .NET Core 以降、非同期データベース操作 (`OpenAsync()`, `ExecuteNonQueryAsync()`, `ExecuteReaderAsync()` など) が広くサポートされています。I/Oバウンドな操作であるデータベースアクセスを非同期化することで、特にWebアプリケーションなどでスレッドをブロックせず、アプリケーションのスケーラビリティと応答性を向上させることができます。

    ```csharp
    // 非同期の例
    public static async Task Main(string[] args)
    {
        using var connection = new SqliteConnection(ConnectionString);
        await connection.OpenAsync();
        // ... 他の非同期操作 ...
    }
    ```

### 2.4. プロフェッショナルな視点

#### 2.4.1. リソース管理とメモリ効率

*   **`using` ステートメントの徹底**: JDBCと同様に、ADO.NETでも `DbConnection`, `DbCommand`, `DbDataReader` などのリソースは使用後に必ず解放しなければなりません。`using` ステートメントを使用することで、確実に `Dispose()` メソッドが呼ばれ、リソースリークを防ぐことができます。
*   **接続プール (Connection Pooling)**: .NETのデータプロバイダ（`SqlConnection`, `SqliteConnection` など）は、既定で接続プールを有効にしています。接続プールは、データベース接続の生成・破棄のオーバーヘッドを削減し、アプリケーションのパフォーマンスを向上させます。接続文字列でプールの設定をカスタマイズすることも可能です。

#### 2.4.2. スレッドセーフティ

*   **`DbConnection` はスレッドセーフではない**: ADO.NETの `DbConnection` オブジェクトも、一般的にスレッドセーフではありません。
*   **各スレッドが自身の `DbConnection` を持つ**: 複数のスレッドで同じ `DbConnection` オブジェクトを共有することは避けるべきです。接続プールを利用している場合でも、`connection.Open()` を呼び出して取得した `DbConnection` インスタンスは、そのスレッド（または非同期コンテキスト）専用として使用し、`connection.Close()` または `Dispose()` で確実にプールに返却する必要があります。

#### 2.4.3. セキュリティ (SQLインジェクション対策)

*   **パラメーター化クエリの絶対的な利用**: ユーザー入力や外部からのデータを用いてSQL文を構築する際は、必ずパラメーター化クエリ (`DbParameter`) を使用してください。パラメーター化クエリは、パラメータ値をSQL文として解釈されることなく安全にデータベースに渡すため、SQLインジェクション攻撃を防ぎます。

    ```csharp
    // 悪い例（SQLインジェクションの脆弱性あり）
    string username = GetUserInput(); // 例: "admin' OR '1'='1"
    string sql = $"SELECT * FROM users WHERE username = '{username}'";
    // new SqliteCommand(sql, connection).ExecuteReader(); // 実行すると危険！
    ```

#### 2.4.4. パフォーマンス

*   **パラメーター化クエリの再利用**: `DbCommand` を作成し、パラメータを設定して繰り返し実行することで、データベース側でクエリの実行計画がキャッシュされ、パフォーマンスが向上する可能性があります。
*   **バッチ処理**: 複数のINSERT/UPDATE/DELETE操作を一度に実行する場合、`DbCommand` のバッチ処理機能（データベースプロバイダによってはサポート）や、複数のSQL文をセミコロンで区切って一度の `ExecuteNonQuery` で実行することで、ネットワークラウンドトリップを減らし、パフォーマンスを向上できます。
*   **適切なデータ取得**: JDBCと同様に、`SELECT *` ではなく、必要なカラムのみを指定して取得することが重要です。
*   **非同期処理**: I/Oバウンドなデータベース操作を `async`/`await` を使って非同期で実行することで、アプリケーションのスケーラビリティと応答性を大幅に向上させることができます。特にGUIアプリケーションやWeb APIでは必須と言えるでしょう。

---

## 3. 共通のベストプラクティス

JavaとC#、どちらのプラットフォームでデータベース接続を行うにしても、共通して適用される重要なベストプラクティスがあります。

### 3.1. 接続文字列の管理

データベースの接続文字列（ユーザー名、パスワード、ホスト名、データベース名など）をコード内に直接ハードコーディングすることは避けてください。

*   **理由**: セキュリティリスク（ソースコードからの情報漏洩）、環境ごとの設定変更の困難さ。
*   **解決策**:
    *   **Java**: `application.properties` (Spring Boot), `log4j2.xml` など設定ファイルから読み込む。または環境変数を使用する。
    *   **C#**: `appsettings.json` (ASP.NET Core), `App.config` (.NET Framework), 環境変数を使用する。
*   **機密情報の保護**: パスワードなどの機密情報は、暗号化して保存したり、AWS Secrets ManagerやAzure Key Vaultのようなシークレット管理サービスを利用したりすることを検討してください。

### 3.2. トランザクション管理の基本

複数のデータベース操作が論理的に一つのまとまりとして扱われるべき場合（例: 注文と在庫更新）、トランザクションを使用します。

*   **目的**: ACID特性（原子性、一貫性、独立性、永続性）を保証し、データ整合性を維持します。
*   **基本的な流れ**:
    1.  `Connection.setAutoCommit(false)` (Java) または `Connection.BeginTransaction()` (C#) でトランザクションを開始します。
    2.  一連のデータベース操作を実行します。
    3.  すべての操作が成功したら `Connection.commit()` で変更を永続化します。
    4.  途中でエラーが発生した場合は `Connection.rollback()` で行った変更をすべて元に戻します。
    5.  最後に `Connection.setAutoCommit(true)` (Java) または `Transaction.Dispose()` (C#) でトランザクションを終了し、`Connection` を閉じます。
*   **注意**: トランザクションはデータベースリソースをロックする可能性があるため、できるだけ短く保つべきです。

### 3.3. エラーハンドリングとログ記録

データベース操作は、ネットワークの問題、データベースサーバーの停止、SQL構文エラー、データ整合性違反など、さまざまな理由で失敗する可能性があります。

*   **適切なエラーハンドリング**:
    *   `SQLException` (Java) や `SqlException` (C#) などの例外をキャッチし、適切に処理します。
    *   ユーザーに対しては、技術的なエラーメッセージではなく、分かりやすいメッセージを表示するようにします。
    *   システム管理者や開発者向けには、詳細なエラー情報（スタックトレース、エラーコードなど）をログに出力します。
*   **ログ記録の徹底**: データベース接続の成功・失敗、実行されたSQL文（機密情報を除く）、トランザクションのコミット・ロールバック、エラー発生時など、重要なイベントをログに記録します。これにより、問題発生時の原因究明が容易になります。
    *   Java: SLF4J + Logback/Log4j2
    *   C#: Microsoft.Extensions.Logging

### 3.4. ORM (Object-Relational Mapping) の活用

アプリケーションが複雑になり、データベースアクセスが多岐にわたる場合、JDBC/ADO.NETの直接利用はコード量が多くなりがちです。

*   **目的**: オブジェクト指向のプログラミング言語とリレーショナルデータベースの間のギャップを埋め、データアクセス層の開発を効率化します。
*   **利点**:
    *   SQLを直接書く機会を減らし、生産性を向上。
    *   オブジェクトとしてデータを扱えるため、コードが読みやすくなる。
    *   データベースプロバイダの変更が容易になる（ベンダーロックインの軽減）。
*   **代表的なORM**:
    *   Java: Hibernate (JPA), Mybatis, jOOQ
    *   C#: Entity Framework Core, Dapper
*   **注意**: ORMは強力ですが、パフォーマンスチューニングが必要な場合や複雑なクエリでは、依然として生のSQLを使用する選択肢も必要になることがあります。ORMを使うかどうかはプロジェクトの規模や特性を考慮して決定しましょう。

---

## まとめ

本Wikiでは、JavaのJDBCとC#のADO.NETを用いたデータベース接続の基本を、即実行可能なコード例とともに解説しました。単にコードを書くだけでなく、以下のプロフェッショナルな視点を常に意識することが重要です。

*   **リソース管理**: `try-with-resources` (Java) や `using` ステートメント (C#) を使い、リソースリークを防ぐ。接続プールの活用。
*   **スレッドセーフティ**: `Connection` はスレッドセーフではないため、スレッドごとに独立した接続を使用する。
*   **セキュリティ**: SQLインジェクションを防ぐため、`PreparedStatement` (Java) やパラメーター化クエリ (C#) を常に使用する。
*   **パフォーマンス**: `PreparedStatement` の再利用、バッチ処理、非同期処理、適切なカラム選択。
*   **保守性**: 接続文字列の外部化、適切なトランザクション管理、堅牢なエラーハンドリングとログ記録。

これらの基本をしっかりと理解し、日々の開発に活かすことで、より堅牢でセキュア、そして高性能なアプリケーションを構築できるようになります。このWikiが皆さんの学習の一助となり、チームの技術力向上に貢献できることを願っています。

疑問点やさらに深く知りたいトピックがあれば、遠慮なくチームのリードエンジニアに相談してください。